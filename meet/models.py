from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html


class Base(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(Base):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Task(Base):
    NOT_STARTED = "NS"
    OPEN = "OP"
    CLOSED = "CL"
    CANCELLED = "CN"
    STATUS = (
        (NOT_STARTED, "Not Started"),
        (OPEN, "Open"),
        (CLOSED, "Closed"),
        (CANCELLED, "Cancelled"),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    status = models.CharField(max_length=120, choices=STATUS, default=NOT_STARTED)
    begin = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    progress = models.TextField(max_length=255, null=True, blank=True)

    def descriptions(self):
        return format_html("<div style='width:220px'>{}</div>", self.description)

    def st(self):
        if self.status == self.NOT_STARTED:
            return "➖"
        elif self.status == self.OPEN:
            return "➗"
        elif self.status == self.CLOSED:
            return "✔️"
        else:
            return "✖️"

    def owner(self):
        return format_html("<div style='min-width:100px'>{}</div>", self.user.get_full_name())

    def end_date(self):
        if (
                (self.status == self.NOT_STARTED or self.status == self.OPEN) and
                self.end and
                self.end < datetime.now().date()
        ):
            return format_html("<div style='min-width:80px;background-color:red;color:#FFF; padding:3px'>{}</div>",
                               self.end)
        return format_html("<div style='min-width:80px'>{}</div>", self.end)

    def begin_date(self):
        return format_html("<div style='min-width:80px'>{}</div>", self.begin)

    def __str__(self):
        return self.description
