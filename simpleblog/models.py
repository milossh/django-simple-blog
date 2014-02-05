from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.SlugField()
    bodytext = models.TextField(verbose_name=_("message"))

    post_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("post date"))
    modified = models.DateTimeField(null=True, verbose_name=_("modified"))
    posted_by = models.ForeignKey('auth.User', verbose_name=_("posted by"))

    allow_comments = models.BooleanField(
        default=True, verbose_name=_("allow comments"))
    comment_count = models.IntegerField(
        blank=True, default=0, verbose_name=_('comment count'))

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-post_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
            'year': '%04d' % self.post_date.year,
            'month': '%02d' % self.post_date.month,
            'day': '%02d' % self.post_date.day,
        }

        return reverse('blog_detail', kwargs=kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', verbose_name=_("post"))
    bodytext = models.TextField(verbose_name=_("message"))

    post_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("post date"))
    ip_address = models.GenericIPAddressField(
        default='0.0.0.0', verbose_name=_("ip address"))

    user = models.ForeignKey(
        'auth.User', null=True, blank=True, verbose_name=_("user"), related_name='comment_user')
    user_name = models.CharField(
        max_length=50, default='anonymous', verbose_name=_("user name"))
    user_email = models.EmailField(blank=True, verbose_name=_("user email"))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['post_date']

from .signals import save_comment

post_save.connect(save_comment, sender=Comment)
