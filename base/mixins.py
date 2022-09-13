

class FieldPermissionSerializerMixin:
    FIELD_PERM_CODENAME = '{model}.can_change_{model}_{name}'
    """
    ModelSerializer logic for marking fields as ``read_only=True`` when a user is found not to have
    change permissions.
    """
    def __init__(self, *args, **kwargs):
        super(FieldPermissionSerializerMixin, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        model = self.Meta.model
        model_field_names = [f.name for f in model._meta.get_fields()]  # this might be too broad
   
        for name in model_field_names:
            perm = f'{model._meta.model_name}.can_change_{model._meta.model_name}_{name}'
            print(perm)
            if name in self.fields and not user.has_perm(perm):

                self.fields[name].read_only = True




