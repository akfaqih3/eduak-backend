from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    Custom field to automatically set the order of an object
    relative to other objects with the same parent.
    """
    
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # No current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # Filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) 
                            for field in self.for_fields}
                    qs = qs.filter(**query)
                # Get the order of the last item
                try:
                    last_item = qs.latest(self.attname)
                    value = last_item.order + 1
                except ObjectDoesNotExist:
                    value = 0
                setattr(model_instance, self.attname, value)
                return value
            except:
                return 0
        else:
            return super().pre_save(model_instance, add)
