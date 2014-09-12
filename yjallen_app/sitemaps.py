import datetime
from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from yjallen_app.models import LetterTitle

class LetterSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return LetterTitle.objects.only('id')

    def location(self, item):
        return reverse('letter_display', args=[item.id])
