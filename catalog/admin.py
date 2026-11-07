from django.contrib import admin
from .models import Course, Inquiry


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "credits", "instructor", "created_at")
    list_filter = ("credits", "instructor")
    search_fields = ("code", "title", "instructor")
    ordering = ("code",)
    readonly_fields = ("created_at",)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("student_name", "email", "course", "is_resolved", "created_at")
    list_filter = ("is_resolved", "course", "created_at")
    search_fields = ("student_name", "email", "message")
    list_editable = ("is_resolved",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    actions = ["mark_resolved", "mark_unresolved"]

    @admin.action(description="Mark selected inquiries as resolved")
    def mark_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f"{updated} inquiries marked as resolved.")

    @admin.action(description="Mark selected inquiries as unresolved")
    def mark_unresolved(self, request, queryset):
        updated = queryset.update(is_resolved=False)
        self.message_user(request, f"{updated} inquiries marked as unresolved.")