from edc_list_data.model_mixins import ListModelMixin
from edc_model.models import BaseUuidModel


class SaeReason(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta, BaseUuidModel.Meta):
        pass
