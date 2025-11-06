"""Forms definitions for UI app."""

from django import forms
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from ui.include import messages
from ui.include.forms import ObjectModelForm


#############################################################################
# Group
#############################################################################


class GroupForm(ObjectModelForm):
    """
    Form for the Django Group model.

    Provides a Many-to-Many field to assign users to the group.

    Attributes:
        users (ModelMultipleChoiceField): Select multiple users for the group.

    Methods:
        __init__(*args, **kwargs): Pre-populates 'users' for existing groups.
        save(commit=True): Saves the group and updates the associated users.
    """

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False, widget=forms.SelectMultiple
    )

    class Meta:
        """
        Meta class for GroupForm.

        Attributes:
            model (Group): The Django Group model this form operates on.
            fields (list[str]): Fields included in the form ('name', 'users').
        """

        model = Group
        fields = ["name", "users"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and pre-fill the 'users' field for existing group instances.
        """
        super().__init__(*args, **kwargs)
        # Pre-populate the users field with those already in the group
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save(self, commit=True):
        """
        Save the group instance and update the associated users.

        Args:
            commit (bool): Whether to commit the changes to the database.

        Returns:
            Group: The saved group instance.
        """
        group = super().save(commit=False)
        if commit:
            group.save()
            group.user_set.set(self.cleaned_data["users"])
        return group


#############################################################################
# User
#############################################################################


class UserForm(ObjectModelForm):
    """
    Form for the Django User model.

    Provides a Many-to-Many field to assign groups to the user.

    Attributes:
        groups (ModelMultipleChoiceField): Select multiple groups for the user.

    Methods:
        __init__(*args, **kwargs): Pre-populates 'groups' for existing user instances.
        save(commit=True): Saves the user and updates the associated groups.
    """

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,
        help_text=messages.PASSWORD1_HELP,
    )

    password2 = forms.CharField(
        label="Conferma Password",
        widget=forms.PasswordInput,
        required=False,
        help_text=messages.PASSWORD2_HELP,
    )

    class Meta:
        """
        Meta class for UserForm.

        Attributes:
            model (User): The Django User model this form operates on.
            fields (list[str]): Fields included in the form:
                'username', 'first_name', 'last_name', 'email', 'is_active',
                'is_superuser', 'is_staff', 'groups'.
        """

        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and pre-fill the 'groups' field for existing users.
        """
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # Pre-populate groups if user exists
        if self.instance.pk:
            self.fields["groups"].initial = self.instance.groups.all()
        if user and not user.is_superuser:
            # Disable field for non admins
            self.fields["groups"].disabled = True
            self.fields["is_staff"].disabled = True
            self.fields["is_superuser"].disabled = True

    def clean(self):
        """
        Check that password1 and password2 match.
        """
        cleaned_data = super().clean()
        user = getattr(self, "current_user", None)
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:  # if one of the two is filled in
            if password1 != password2:
                raise forms.ValidationError(messages.PASSWORD_ERROR)

        if user and not user.is_superuser and self.instance.pk:
            # Disable field for non admins
            cleaned_data["is_staff"] = getattr(self.instance, "is_staff")
            cleaned_data["is_superuser"] = getattr(self.instance, "is_superuser")
            cleaned_data["groups"] = getattr(self.instance, "is_superuser")

        return cleaned_data

    def save(self, commit=True):
        """
        Save the user instance and update the associated groups.

        Args:
            commit (bool): Whether to commit the changes to the database.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)

        password1 = self.cleaned_data.get("password1")
        if password1:  # only if set/modified
            user.set_password(password1)

        if commit:
            user.save()
            user.groups.set(self.cleaned_data["groups"])
        return user



#############################################################################
# Token
#############################################################################


class TokenForm(ObjectModelForm):
    """
    Form for the Django Token model.
    """

    class Meta:
        """
        Meta class for TokenForm.
        """

        model = Token
        fields = []
