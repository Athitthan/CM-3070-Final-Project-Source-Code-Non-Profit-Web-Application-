from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.utils import timezone


# Create your models here.


# ---I WROTE THIS CODE---
# Model representing an application user
class AppUser(models.Model):
    CATEGORY_CHOICES = (
        ("patient", "patient"),
        ("volunteer", "volunteer"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    background_image = models.ImageField(null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    group = models.CharField(
        max_length=20, null=False, blank=False, choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.user.username


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing the status of an application user
class Status(models.Model):
    status = models.TextField(
        null=True, blank=True, default=None
    )  # Field to store long sentences
    created_at = models.DateTimeField(auto_now_add=True)
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing user posts in a gallery
class Gallery(models.Model):
    post_media = models.FileField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing user followings
class Followings(models.Model):
    current_user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="followings_current_user"
    )
    following = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="followings_following"
    )

    class Meta:
        unique_together = ("current_user", "following")


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing user requests
class Request(models.Model):
    requested_user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="requested_users"
    )
    requester = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="requesters"
    )

    class Meta:
        unique_together = ("requested_user", "requester")


# ---END OF CODE THAT I WROTE---


# ---I WROTE THIS CODE---
# Model representing chat messages
class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


# ---END OF CODE THAT I WROTE---


# Model representing Forum Posts
class ForumPost(models.Model):
    CATEGORY_CHOICES = (
        ("treatment", "Treatment Options"),
        ("lifestyle", "Lifestyle Adjustments"),
        ("emotional", "Emotional Support"),
        ("challenges", "Daily Challenges"),
    )

    

    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    creator = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title


# Model representing Post Comments
class Comment(models.Model):
    post = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="comments"
    )
    creator = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.creator.name} on {self.post.title}"


# Model representing comment replies
class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    creator = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.creator.name} on {self.comment.post.title}"


# Model representing Volunteer Tasks
class VolunteerHelp(models.Model):
    CATEGORY_CHOICES = (
        ("grocery", "Help with groceries"),
        ("house_cleaning", "Help with house cleaning"),
        ("emotional", "Provide emotional help"),
        ("others", "Help with specific tasks"),
    )

    # A subset example of locations/towns in Singapore
    SINGAPORE_LOCATIONS = (
        ("Sembawang", "Sembawang"),
        ("Woodlands", "Woodlands"),
        ("Yishun", "Yishun"),
        ("Ang Mo Kio", "Ang Mo Kio"),
        ("Hougang", "Hougang"),
        ("Punggol", "Punggol"),
        ("Sengkang", "Sengkang"),
        ("Serangoon", "Serangoon"),
        ("Bedok", "Bedok"),
        ("Pasir Ris", "Pasir Ris"),
        ("Tampines", "Tampines"),
        ("Bukit Batok", "Bukit Batok"),
        ("Bukit Panjang", "Bukit Panjang"),
        ("Choa Chu Kang", "Choa Chu Kang"),
        ("Clementi", "Clementi"),
        ("Jurong East", "Jurong East"),
        ("Jurong West", "Jurong West"),
        ("Tengah", "Tengah"),
        ("Central", "Central"),
        ("Bishan", "Bishan"),
        ("Bukit Merah", "Bukit Merah"),
        ("Bukit Timah", "Bukit Timah"),
        ("Central Area", "Central Area"),
        ("Geylang", "Geylang"),
        ("Kallang/ Whampoa", "Kallang/ Whampoa"),
        ("Marine Parade", "Marine Parade"),
        ("Queenstown", "Queenstown"),
        ("Toa Payoh", "Toa Payoh"),
    )

    user = models.ForeignKey(AppUser, related_name="patients", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    preferred_date_time = models.DateTimeField(null=False, blank=False)
    duration = models.DecimalField(
        max_digits=3, decimal_places=1, null=False, blank=False
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    volunteer_limit = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="At least 1 volunteer is required."),
            MaxValueValidator(5, message="No more than 5 volunteers allowed."),
        ]
    )  # Field for the preferred number of volunteers
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(     max_length=50,
        choices=SINGAPORE_LOCATIONS,
        help_text="Select a location in Singapore",
        
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.user.group == "patient":
            raise ValidationError("Only patients can register for volunteer help.")
        super(VolunteerHelp, self).save(*args, **kwargs)


# Model representing Volunteered Helps
class VolunteeredHelp(models.Model):
    volunteer_help = models.ForeignKey(
        VolunteerHelp, related_name="volunteer_helps", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        AppUser, related_name="volunteers", on_delete=models.CASCADE
    )

    preferred_date_time_field_changed = models.BooleanField(default=False)
    title_field_changed = models.BooleanField(default=False)
    description_field_changed = models.BooleanField(default=False)
    duration_field_changed = models.BooleanField(default=False)
    volunteer_limit_field_changed = models.BooleanField(default=False)
    location_field_changed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.user.group == "volunteer":
            raise ValidationError("Only volunteers can commit to volunteer help.")
        super(VolunteeredHelp, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("volunteer_help", "user")


# Model representing disease overview content
class DiseaseOverview(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)


# Model representing disease research update content
class ResearchUpdate(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    publication_date = models.DateField()
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


# Model representing other patients story content
class PatientStory(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    story = models.TextField()
    date_shared = models.DateField()
    image = models.ImageField(null=True, blank=True)
