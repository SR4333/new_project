import hmac
import uuid
from django.db import models
#from django.contrib.gis.db import models as gis_models

from new_app.models import CustomUser
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from django.db import connection, models
#from django.db.models import Manager as GeoManager
from common.constants import SUPPORT_COUNTRIES
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

'''# Create your models here.
SUPPORT_MSG_LANGUAGES_CHOICE = (
    ("english", "English"),
    ("greek", "Greek"),
    ("portuguese", "Portuguese"),
    ("turkish", "Turkish"),
    ("italian", "Italian"),
    ("spanish", "Spanish"),
    ("french", "French"),
    ("russian", "Russian"),
    ("indonesian", "Indonesian"),
    ("german", "German"),
    ("hungarian", "Hungarian"),
    ("ukrainian", "Ukrainian"),
    ("romanian", "Romanian"),
)


class BaseModel(models.Model):
    """
    Base Model with created_at, and modified_at fields, will be inherited
    in all other models.
    """

    meta_created_ts = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Meta Created TimeStamp"),
        null=True,
        blank=True,
    )
    meta_updated_ts = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name=_("Meta Updated TimeStamp"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
CONTENT_TYPE_CHOICES = (
    ("terms_and_conditions", "Terms and Conditions"),
    ("privacy_policy", "Privacy Policy"),
    ("disclaimer", "Disclaimer"),
    ("privacy_consent", "Privacy Consent"),
)

# AL-3885
THRESHOLD_REFERENCE_TYPE = (
    ("daily_average_count", _("Daily Average Count")),
    ("cumulative_count", _("Cumulative Count")),
    ("incremental_count", _("Incremental Count")),
    ("actual_count", _("Actual Count")),
)


def country_flag_file_name(instance, filename):
    if instance.id:
        return "/".join(
            [
                connection.schema_name,
                "countryflagimage",
                str(instance.id),
                str(filename),
            ]
        )
    else:
        new_uuid = uuid.uuid4()
        return "/".join(
            [
                connection.schema_name,
                "countryflagimage",
                hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest(),
                str(filename),
            ]
        )

class Country(BaseModel):

    DATE_PREFERENCES = (
        ("MDY", _("Month, Day and Year")),
        ("DMY", _("Day, Month and Year")),
        ("YMD", _("Year, Month and Day")),
        ("YDM", _("Year, Day and Month")),
    )
    TIME_PREFERENCES = (
        ("12_hour_clock", _("12 hour clock")),
        ("24_hour_clock", _("24 hour clock")),
    )
    AREA_MEASUREMENT_PREFERENCES = (
        ("hectares", _("Hectares")),
        ("acres", _("Acres")),
    )
    CONSENT_TYPES = (
        ("acknowledgement", _("Acknowledgement")),
        ("consent", _("Consent")),
        ("no_consent", _("No Consent")),
    )
    name = models.CharField(max_length=100, unique=True)
    phone_code = models.CharField(max_length=10, null=True, blank=True)
    flag_image = models.FileField(
        upload_to=country_flag_file_name, blank=True, null=True
    )
    is_active = models.BooleanField(default=False)
    trap_name_visibility_threshold = models.FloatField(default=0, null=True, blank=True)
    trap_clickable_threshold = models.FloatField(default=0, null=True, blank=True)
    grower_profile_completeness = models.BooleanField(default=False)

    # AL-2293: Add fields to set the season start and end date
    season_start_date = models.DateField(
        verbose_name=_("Season start date"),
        null=True,
        blank=True,
    )
    season_end_date = models.DateField(
        verbose_name=_("Season end date"),
        null=True,
        blank=True,
    )

    # AL-2264: Add fields for measurement system
    measurement_system = models.CharField(
        default="metric",
        max_length=25,
        verbose_name=_("Measurement system"),
        null=True,
        blank=True,
        choices=[("imperial", "imperial"), ("metric", "metric")],
    )

    # AL-2264: Add fields for date style
    date_preference = models.CharField(
        default="DMY",
        max_length=15,
        verbose_name=_("Date Preference"),
        null=True,
        blank=True,
        choices=DATE_PREFERENCES,
    )

    # zoom fields
    default_zoom_level = models.FloatField(default=9, null=True, blank=True)
    min_zoom_level = models.FloatField(default=6.5, null=True, blank=True)
    max_zoom_level = models.FloatField(default=18.75, null=True, blank=True)

    # Message portal flag
    is_message_portal_enabled = models.BooleanField(default=False)

    # AL-4090 - Add a flag to skip the SMS validation during sign-up
    skip_sms_validation = models.BooleanField(default=False)

    # AL-4059 - Add a flag to enable in app scouting
    is_in_app_scouting_enabled = models.BooleanField(default=False)

    # User Data Retention Days
    user_data_retention_duration_in_years = models.IntegerField(
        default=0, null=True, blank=True
    )

    # AL-3877 - Add a new flag in country table: “Track Users Location Enabled”
    track_users_location_enabled = models.BooleanField(default=False)

    # AL-4104 - Required form fields
    enable_farms_and_fields_for_scouting = models.BooleanField(default=True)

    # AL-4448 - Show/hide the Farm field at the country level
    enable_farm_entry = models.BooleanField(default=False)

    # AL-4532 - Add field for time format
    time_preference = models.CharField(
        max_length=20, default="12_hour_clock", blank=True, choices=TIME_PREFERENCES
    )

    # AL-4853 - Ability to toggle between Hectares/Acres
    area_measurement_unit = models.CharField(
        max_length=20, default="hectares", choices=AREA_MEASUREMENT_PREFERENCES
    )

    # AL-5087 - Add flag to enable/disable field monitoring
    field_monitoring_enabled = models.BooleanField(default=False)

    # AL-5194 - consent checkboxes based on country laws
    consent_type = models.CharField(
        max_length=20,
        default="acknowledgement",
        choices=CONSENT_TYPES,
        help_text="Determines what type of data privacy consent this country requires for sign-up",
    )

    # AL-5355 - pilot country flag and pilot country code
    is_pilot_country = models.BooleanField(default=False)
    pilot_country_code = models.CharField(max_length=100, null=True, blank=True)

    # AL-5987 Message portal v2 flag
    is_message_portal_v2_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class State(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Crop(BaseModel):
    """
    Crop Model stores the names of all the existing crops
    May be modified to accommodate additional fields
    """

    crop_name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.crop_name)

class Pest(BaseModel):
    """
    Pest Model stores the names of all the existing pests
    May be modified later to accommodate additional fields
    """

    scientific_name = models.CharField(max_length=100, null=True, blank=True)
    common_name = models.CharField(max_length=100, null=True, blank=True)
    family = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    upper_threshold_temp = models.PositiveIntegerField(null=True, blank=True)
    lower_threshold_temp = models.PositiveIntegerField(null=True, blank=True)
    # AL-4581
    send_images_to_CV = models.BooleanField(default=False)

    # AL-4761
    rank = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="The highest rank will be displayed first in the Arc App",
        verbose_name="The highest rank will be displayed first in the Arc App",
    )

    def __str__(self):
        return "{}".format(self.common_name)

class Region(BaseModel, gis_models.Model):
    """
    Region Model stores the region information for the owners
    May be modified to accommodate additional fields later
    """

    gis = GeoManager()
    objects = models.Manager()

    name = models.CharField(max_length=100, null=False, blank=False)
    coordinates = gis_models.PolygonField(
        srid=4326,
        null=True,
        blank=True,
    )
    user = models.ManyToManyField(
        CustomUser,
        through="fields.UserRegion",
        related_name="user_region",
    )
    state = models.CharField(max_length=50, blank=True, null=True)
    state_fk = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=50, choices=SUPPORT_COUNTRIES)
    country_fk = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    language = models.CharField(
        max_length=255, choices=SUPPORT_MSG_LANGUAGES_CHOICE, null=True, blank=True
    )
    timezone = models.CharField(max_length=255, null=True, blank=True)
    timeformat = models.CharField(max_length=255, null=True, blank=True)
    dateformat = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    trap_name_visibility_threshold = models.FloatField(default=0, null=True, blank=True)
    trap_clickable_threshold = models.FloatField(default=0, null=True, blank=True)
    has_trap_catch_graph = models.BooleanField(default=True)
    has_egg_count_graph = models.BooleanField(default=True)
    has_larvae_count_graph = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "state_fk")

    def __str__(self):
        return "{}".format(self.name)'''
