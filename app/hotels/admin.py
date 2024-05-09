from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Hotel, HotelChain, HotelDraft


class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 0
    fields = ("name", "location", "is_active")


@admin.register(HotelChain)
class HotelChainAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price_range",
        "recipient_email",
        "created_at",
        "updated_at",
    )
    list_filter = ("price_range", "auto_assign")
    search_fields = ("title",)
    search_help_text = "Search for a hotel chain title"
    list_filter = ("price_range",)

    fieldsets = (
        ("Chain Information", {"fields": ("title", "price_range", "description")}),
        (
            "Contact",
            {
                "fields": ("email", "phone", "sales_contact", "website"),
                "classes": ("collapse",),
                "description": "Email to receive notifications when a hotel is created",
            },
        ),
        (
            "Auto Assign",
            {
                "fields": ("auto_assign", "recipient_email"),
                "classes": ("collapse",),
            },
        ),
    )
    inlines = [HotelInline]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "image",
        "name",
        "location",
        "chain",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "chain")
    search_fields = ("name",)
    search_help_text = "Search for a hotel name"

    fieldsets = (
        ("Hotel Information", {"fields": ("name", "location", "photo")}),
        ("Chain", {"fields": ("chain",), "description": "The chain of the hotel"}),
        (
            "Status",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "Related Hotels",
            {
                "fields": ("related_hotels",),
                "classes": ("collapse",),
            },
        ),
    )

    def image(self, obj):
        if not obj.photo:
            return "No photo"
        return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')

    def hotel_make_active(self, request, queryset):
        queryset.update(is_active=True)

    def hotel_make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    actions = [hotel_make_active, hotel_make_inactive]  # type: ignore
    hotel_make_active.short_description = "Activate selected Hotels"
    hotel_make_inactive.short_description = "Deactivate selected Hotels"


@admin.register(HotelDraft)
class HotelDraftAdmin(admin.ModelAdmin):
    list_display = (
        "hotel__name",
        "chain__title",
        "status_icon",
        "created_by",
        "created_at",
        "updated_at",
        "hotel_url",
        "draft_actions",
    )
    list_filter = ("status", "hotel__is_active", "hotel__chain__price_range")
    search_fields = ("hotel__name", "hotel__location", "hotel__chain__title")
    search_help_text = "Search for a hotel name"
    fieldsets = (
        ("Hotel Draft", {"fields": ("hotel", "status", "created_by")}),
        (
            "Update",
            {
                "fields": ("name", "location", "photo", "chain", "is_active"),
                "description": "The fields to update in the hotel",
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at", "status")

    def chain__title(self, obj):
        if obj.status == HotelDraft.STATUS_APPROVED and not obj.chain.title:
            return "-"

        if obj.status == HotelDraft.STATUS_APPROVED:
            return obj.chain.title + " (Approved)"

        if not obj.status == HotelDraft.STATUS_APPROVED and not obj.chain:
            return "-"
        return obj.chain.title + f" ({obj.status})"

    def hotel__name(self, obj):
        return obj.hotel.name

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:hotel_draft_id>/approve_form/",
                self.admin_site.admin_view(self.approve_form),
                name="approve_form",
            ),
            path(
                "<int:hotel_draft_id>/reject/",
                self.admin_site.admin_view(self.save_as_reject),
                name="save_as_reject",
            ),
            path(
                "<int:hotel_draft_id>/pending/",
                self.admin_site.admin_view(self.save_as_pending),
                name="save_as_pending",
            ),
        ]
        return custom_urls + urls

    @admin.display(description="Actions")
    def draft_actions(self, obj):
        if obj.status == HotelDraft.STATUS_APPROVED:
            all_actions = [f'<a href="{obj.id}/delete">🗑️</a>']
        else:
            all_actions = [
                f'<a href="{obj.id}/approve_form/">✅ Approve</a>',
                f'<a href="{obj.id}/reject/">❌ Reject</a>',
                f'<a href="{obj.id}/pending/">⏳ Pending</a>',
            ]

        return mark_safe(" | ".join(all_actions))

    @admin.display(description="Status")
    def status_icon(self, obj):
        if obj.status == HotelDraft.STATUS_APPROVED:
            return "✅"
        if obj.status == HotelDraft.STATUS_REJECTED:
            return "❌"
        return "⏳"

    def hotel_url(self, obj):
        url = reverse("admin:hotels_hotel_change", args=[obj.hotel.id])
        return mark_safe(f'<a href="{url}">🔗</a>')

    def approve_form(self, request, hotel_draft_id):
        if not request.user.is_reviewer and not request.user.is_superuser:
            self.message_user(
                request, "You are not allowed to approve hotel drafts", level="ERROR"
            )
            return redirect("admin:hotels_hoteldraft_change", hotel_draft_id)  # type: ignore

        hotel_draft = HotelDraft.objects.get(id=hotel_draft_id)
        hotel_draft.status = HotelDraft.STATUS_PENDING
        hotel_draft.save()

        if request.method == "POST":
            updated = hotel_draft.approved_and_save()

            if bool(updated):
                self.message_user(request, "Hotel Draft has been approved and updated")
                return redirect("admin:hotels_hoteldraft_changelist")  # type: ignore
            else:
                self.message_user(
                    request,
                    "Hotel Draft has been approved but no changes were made",
                    level="ERROR",
                )
                return redirect("admin:hotels_hoteldraft_changelist")

        context = dict(
            self.admin_site.each_context(request),
            title="Approve Hotel Draft?",
            object=hotel_draft,
            opts=self.model._meta,
        )

        return TemplateResponse(
            request, "admin/hotels/hoteldraft/approve_form.html", context
        )

    def save_as_pending(self, request, hotel_draft_id):
        hotel_draft = HotelDraft.objects.get(id=hotel_draft_id)
        hotel_draft.status = HotelDraft.STATUS_PENDING
        hotel_draft.save()
        return redirect("admin:hotels_hoteldraft_changelist")  # type: ignore

    def save_as_reject(self, request, hotel_draft_id):
        hotel_draft = HotelDraft.objects.get(id=hotel_draft_id)
        hotel_draft.status = HotelDraft.STATUS_REJECTED
        hotel_draft.save()

        self.message_user(request, "Hotel Draft has been rejected")
        return redirect("admin:hotels_hoteldraft_changelist")  # type: ignore

    # def make_approve(self, request, queryset):
    #    queryset.update(status=HotelDraft.STATUS_APPROVED)

    def make_reject(self, request, queryset):
        queryset.update(status=HotelDraft.STATUS_REJECTED)

    def make_pending(self, request, queryset):
        queryset.update(status=HotelDraft.STATUS_PENDING)

    actions = [  # type: ignore
        make_pending,
        # make_approve,
        make_reject,
    ]
    # make_approve.short_description = "Approve selected Hotel Drafts"
    make_reject.short_description = "Reject selected Hotel Drafts"
    make_pending.short_description = "Pending selected Hotel Drafts"
