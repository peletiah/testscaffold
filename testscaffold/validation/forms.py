# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import wtforms
import marshmallow
from testscaffold.validation import ZigguratForm
from testscaffold.validation.schemes import (UserCreateSchema,
                                             UserEditSchema,
                                             GroupEditSchema)

from testscaffold.models.user import User


def strip_filter(value):
    return value.strip() if value else None


def validate_marshmallow_partial(schema):
    """ This attempts to validate a single node of a schema
        of same name as wtform field name, form context is passed to schema """

    def _validator(form, field):
        schema_inst = schema(context=form.context)
        try:
            schema_inst.load({field.name: field.data}, partial=True)
        except marshmallow.ValidationError as exc:
            raise wtforms.ValidationError(', '.join(exc.messages[field.name]))

    return _validator


class UserCreateForm(ZigguratForm):
    user_name = wtforms.StringField(
        "User name",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            validate_marshmallow_partial(UserCreateSchema)])
    password = wtforms.PasswordField(
        "Password",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            validate_marshmallow_partial(UserCreateSchema)])
    email = wtforms.StringField(
        "Email",
        filters=[strip_filter],
        validators=[wtforms.validators.InputRequired(),
                    validate_marshmallow_partial(UserCreateSchema)])


class UserLoginForm(ZigguratForm):
    login = wtforms.StringField(
        "Login",
        filters=[strip_filter],
        validators=[wtforms.validators.InputRequired(),
                    wtforms.validators.Length(min=3)])

    password = wtforms.PasswordField(
        "Password",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            wtforms.validators.Length(min=3)])


class UserLostPasswordForm(ZigguratForm):
    email = wtforms.StringField(
        "Email",
        filters=[strip_filter],
        validators=[wtforms.validators.InputRequired(),
                    wtforms.validators.Email()])


class UserNewPasswordForm(ZigguratForm):
    password = wtforms.PasswordField(
        "Password",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            validate_marshmallow_partial(UserEditSchema)])
    password_confirm = wtforms.PasswordField(
        "Confirm password",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            wtforms.validators.EqualTo('password')])


class UserAdminCreateForm(UserCreateForm):
    pass


class UserAdminUpdateForm(UserAdminCreateForm):
    password = wtforms.PasswordField(
        "Password",
        filters=[strip_filter],
        validators=[
            wtforms.validators.Optional(),
            wtforms.validators.Length(min=3)])


class GroupUpdateForm(ZigguratForm):
    group_name = wtforms.StringField(
        "name",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            validate_marshmallow_partial(GroupEditSchema)])

    description = wtforms.TextAreaField(
        "description",
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
        ])


group_permission_choices = []

for permission in User.__possible_permissions__:
    group_permission_choices.append((permission,
                                     permission.title().replace('_', ' '),))


class DirectPermissionForm(ZigguratForm):
    permission = wtforms.SelectField('Permission',
                                     choices=group_permission_choices)
