from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
import csv
# Register your models here.
from .models import Application, JobPosting, Message
admin.site.register(Message)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at",
                    "applicant_name", "applicant_email", "status")
    list_filter = ("status", "created_at", "applicant_email", "applicant_name")
    search_fields = ("applicant_name", "applicant_email")

    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        filename = f"applications_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Created At",
            "Last Updated",
            "Candidate Name",
            "Candidate Email",
            "Application Status",
        ])

        qs = queryset.select_related("candidate")
        for event in qs:
            writer.writerow([
                event.id,
                event.created_at,
                event.updated_at,
                event.applicant_name,
                event.applicant_email,
                event.status,
            ])

        return response

    export_to_csv.short_description = "Export selected applications to CSV"


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "location", "created_at", "created_by","description")
    search_fields = ("title", "company", "location")
    list_filter = ("company", "created_at")
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        filename = f"applications_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Created At",
            "Company",
            "Location",
            "Description",
            "Created By",
        ])

        qs = queryset.select_related("created_by")
        for event in qs:
            writer.writerow([
                event.id,
                event.created_at,
                event.company,
                event.location,
                event.description,
                event.created_by,
                event.title,
            ])

        return response

    export_to_csv.short_description = "Export selected applications to CSV"

