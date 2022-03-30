import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TagBase, TaggedItemBase


class UserTag(TagBase):

    # Add method for saving tags to Employee class
    @classmethod
    def saveToClass(cls, name, *args, **kwargs):
        tag_existed = UserTag.objects.filter(name=name).first()
        if tag_existed:
            return None
        UserTag(name=name).save()
        return 1


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    # If you only inherit GenericUUIDTaggedItemBase, you need to define
    # a tag field. e.g.
    # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)
    tag = models.ForeignKey(UserTag, related_name="%(app_label)s_%(class)s_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
