from django import forms
from django.apps import apps as django_apps
from edc_action_item.forms import ActionItemFormMixin
from edc_constants.constants import CLOSED, OTHER
from edc_form_validators import FormValidator, FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin


class DefaultDeathReportFormValidator(FormValidator):
    @property
    def cause_of_death_model_cls(self):
        return django_apps.get_model("edc_adverse_event.causeofdeath")

    def clean(self):

        self.validate_study_day_with_datetime(
            study_day=self.cleaned_data.get("study_day"),
            compare_date=self.cleaned_data.get("death_datetime"),
            study_day_field="study_day",
        )

        other = self.cause_of_death_model_cls.objects.get(name=OTHER)
        self.validate_other_specify(
            field="cause_of_death",
            other_specify_field="cause_of_death_other",
            other_stored_value=other.name,
        )

        self.required_if(
            CLOSED, field="report_status", field_required="report_closed_datetime"
        )


class DeathReportModelFormMixin(SiteModelFormMixin, ActionItemFormMixin, FormValidatorMixin):

    form_validator_cls = DefaultDeathReportFormValidator

    subject_identifier = forms.CharField(
        label="Subject identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )
