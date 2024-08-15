# wibu_catalog/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# import data from constant
from wibu_catalog.constants import Role_dict, Score_dict
from wibu_catalog.constants import ITEMS_PER_PAGE, Content_category
from wibu_catalog.constants import Manga_status, Anime_status
from wibu_catalog.constants import Manga_rating, Anime_rating
from wibu_catalog.constants import FIELD_MAX_LENGTH_S, FIELD_MAX_LENGTH_M
from wibu_catalog.constants import FIELD_MAX_LENGTH_L, FIELD_MAX_LENGTH_XL

# turn coca into tuple to use with choices
Content_category_tuple = [
    (key, value) for key, value in Content_category.items()
]


class Content(models.Model):
    """Model representing a content."""
    cid = models.IntegerField(
        primary_key=True,
        help_text=_("Content's primary key."),
    )
    category = models.CharField(
        max_length=FIELD_MAX_LENGTH_M,
        null=True,
        choices=Content_category_tuple,
        default='anime',
        help_text=_("Content category"),
    )
    name = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("Content name"),
    )
    scoreAvg = models.FloatField(
        default=0.0,
        null=True,
    )
    genres = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=_("Content's Genres"),
    )
    cType = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Anime type (TV, Movie, OVA,...)")
            if category == '1'
            else _("Manga type (Oneshot, shounen,...)")
        ),
    )
    episodes = models.IntegerField(
        blank=True,
        null=True,
        help_text=(
            _("Number of aired episodes.")
            if category == '1'
            else _("Number of published chapters.")
        ),
    )
    aired = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Broadcast date.")
            if category == '1'
            else _("Publish date.")
        ),
    )
    lastUpdate = models.DateField(
        blank=True,
        null=True,
        help_text=(
            _("Date of last realese episode.")
            if category == '1'
            else _("Date of last published chapter.")
        ),
    )
    producers = models.CharField(
        max_length=FIELD_MAX_LENGTH_XL,
        blank=True,
        null=True,
        help_text=(
            _("Individuals or companies that fund, "
              "organize, and oversee the production of the anime.")
            if category == '1'
            else _("None for Manga.")
        ),
    )
    licensors = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Companies that acquire the rights to distribute the anime.")
            if category == '1'
            else _("Companies that have the rights to translate, "
                   "publish, and distribute the manga.")
        ),
    )
    studios = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Companies responsible for the animation production.")
            if category == '1'
            else _("Tteams that assist the main artist with tasks.")
        ),
    )
    source = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Manga, Light novel, Book, etc. (e.g Original).")
            if category == '1'
            else _("Light novel, Book, etc. (e.g Original).")
        ),
    )
    duration = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Duration of the anime per episode (e.g 24 min. per ep.).")
            if category == '1'
            else _("None for Manga.")
        ),
    )
    rating = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=(
            _("Age rate (e.g. R - 17+ (violence & profanity)).")
            if category == '1'
            else _("Manga age rate (e.g. safe).")
        ),
    )
    ranked = models.IntegerField(  # create a ranked function ticket later
        default=0,
        null=True,
        help_text=(
            _(".")
            if category == '1'
            else _(".")
        ),
    )
    favorites = models.IntegerField(
        default=0,
        null=True,
        help_text=(
            _("Number of user have this anime in their favorite list.")
            if category == '1'
            else _("Number of user have this manga in their favorite list.")
        ),
    )
    watching = models.IntegerField(
        default=0,
        null=True,
        help_text=(
            _("Watching.")
            if category == '1'
            else _("Reading.")
        ),
    )
    completed = models.IntegerField(
        default=0,
        null=True,
        help_text=_("Completed."),
    )
    onHold = models.IntegerField(
        default=0,
        null=True,
        help_text=_("On Hold."),
    )

    dropped = models.IntegerField(
        default=0,
        null=True,
        help_text=_("Dropped."),
    )
    planToWatch = models.IntegerField(
        default=0,
        null=True,
        help_text=(
            _("Plan to Watch.")
            if category == '1'
            else _("Plan to Read.")
        ),
    )
    picture = models.ImageField(
        default=None,
        blank=True,
        null=True,
        help_text=_("Content cover picture."),
    )

    def get_absolute_url(self):
        """Returns the url to access a detail record for this content."""
        return reverse("content-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Score(models.Model):
    """Model representing the scores for a content."""
    score10 = models.IntegerField(
        default=0,
        null=True,
    )
    score9 = models.IntegerField(
        default=0,
        null=True,
    )
    score8 = models.IntegerField(
        default=0,
        null=True,
    )
    score7 = models.IntegerField(
        default=0,
        null=True,
    )
    score6 = models.IntegerField(
        default=0,
        null=True,
    )
    score5 = models.IntegerField(
        default=0,
        null=True,
    )
    score4 = models.IntegerField(
        default=0,
        null=True,
    )
    score3 = models.IntegerField(
        default=0,
        null=True,
    )
    score2 = models.IntegerField(
        default=0,
        null=True,
    )
    score1 = models.IntegerField(
        default=0,
        null=True,
    )
    cid = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='score_data',
    )

    def __str__(self):
        return f"Scores for Content CID: {str(self.cid)}"


Role_tuple = [(key, value) for key, value in Role_dict.items()]


class Users(models.Model):
    """Model representing a user."""
    uid = models.IntegerField(
        primary_key=True,
        help_text=_("User id"),
    )
    username = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("Username"),
    )
    role = models.CharField(
        max_length=FIELD_MAX_LENGTH_M,
        null=True,
        choices=Role_tuple,
        default='new_user',
        help_text=_("User role."),
    )
    email = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("Email address"),
    )
    password = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("Password"),
    )
    dateOfBirth = models.DateField(
        blank=True,
        null=True,
        help_text=_("Date of birth"),
    )
    profilePicture = models.ImageField(
        blank=True,
        null=True,
        help_text=_("Profile picture"),
    )
    registrationDate = models.DateField(
        help_text=_("Account's registration date"),
        null=True,
    )

    def __str__(self):
        return self.username


class FavoriteList(models.Model):
    uid = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='favlist'
    )
    cid = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='favlist'
    )

    contentStatus = (
        (1, "Watching"),
        (2, "Completed"),
        (3, "On_Hold"),
        (4, "Dropped"),
        (5, "Re_Watching"),
        (6, "Plan_to_Watch"),
    )
    status = models.CharField(
        max_length=FIELD_MAX_LENGTH_S,
        choices=contentStatus,
        null=True,
        default='1',
        help_text=_("User status with this content."),
    )
    progress = models.IntegerField(
        default='0',
        null=True,
        help_text=_("User's progress (e.g. chapter01)."),
    )

    def save(self, *args, **kwargs):
        if self.pk:  # Checking if the instance is being updated
            old_fav_list = favorite_list.objects.get(pk=self.pk).status
            update_content_fav_sta(self.cid, self.Status, old_fav_list)
        else:
            # For new instance creation, only update the content table
            update_content_fav_sta(self.cid, self.status)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.status


Score_tuple = [(key, value) for key, value in Score_dict.items()]


class ScoreList(models.Model):
    """Model representing scores given by users to content."""
    uid = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='scoreslist',
    )
    cid = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='scoreslist',
    )
    score = models.IntegerField(
        choices=Score_tuple,
        null=True,
        default='10',
        help_text=_("User's score of this content."),
    )

    class Meta:
        unique_together = ('uid', 'cid')
        # Ensure that each user can score each content only once

    def save(self, *args, **kwargs):
        if self.pk:  # Checking if the instance is being updated
            old_score = score_list.objects.get(pk=self.pk).score
            update_score_table(self.cid, self.score, old_score)
        else:
            # For new instance creation, only update the score table
            update_score_table(self.cid, self.score)

        super().save(*args, **kwargs)
        # Update content score after saving
        update_content_score(self.cid)

    def __str__(self):
        return self.score


class Comments(models.Model):
    """Model representing comments on content."""
    uid = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    cid = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("User's comment."),
    )
    dateOfCmt = models.DateField(
        blank=True,
        null=True,
        help_text=_("Comment's date."),
    )
    likes = models.IntegerField(
        default=0,
        null=True,
        help_text=_("Number of likes."),
    )

    def __str__(self):
        return f"{str(self.uid)},{str(self.cid)},{self.content}"


class Notifications(models.Model):
    """Model representing notifications for users."""
    notificationId = models.AutoField(
        primary_key=True,
        help_text=_("Naughtyfication id."),
    )
    message = models.TextField(
        max_length=FIELD_MAX_LENGTH_XL,
        null=True,
        help_text=_("Notification's message."),
    )
    date = models.DateField(
        null=True,
        help_text=_("Notification's arrived date."),
    )
    nType = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        blank=True,
        null=True,
        help_text=_("Notification's type."),
    )
    isRead = models.BooleanField(
        default=False,
        null=True,
        help_text=_("Notification's is readed by user or not."),
    )
    uid = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='notifications',
    )

    def __str__(self):
        return self.notificationId


class Product(models.Model):
    """Model representing a product related to content."""
    pid = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("Name of the product."),
    )
    price = models.FloatField(
        default=0,
        null=True,
        help_text=_("Product's price."),
    )
    description = models.TextField(
        max_length=FIELD_MAX_LENGTH_XL,
        blank=True,
        null=True,
        help_text=_("Product's description.")
    )
    ravg = models.FloatField(
        default=0,
        null=True,
        help_text=_("Product's average rating."),
    )
    picture = models.ImageField(
        blank=True,
        null=True,
        help_text=_("Product's picture."),
    )
    cid = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.pid


class Order(models.Model):
    """Model representing orders made by users."""
    oid = models.IntegerField(
        primary_key=True,
        help_text=_("Order id."),
    )
    orderDate = models.DateField(
        help_text=_("Date of the order."),
        null=True,
    )
    status = models.CharField(
        max_length=FIELD_MAX_LENGTH_L,
        null=True,
        help_text=_("Order status (e.g. Shipped)."),
    )
    uid = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    def __str__(self):
        return f"Order {self.oid} by User {self.uid}"


class OrderItems(models.Model):
    """Model representing items in an order."""
    oid = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    pid = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    quantity = models.IntegerField(
        default=1,
        null=True,
        help_text=_("Number of ordered products."),
    )
    buyPrice = models.FloatField(
        help_text=_("Price at the time of Ordered."),
        null=True,
    )

    def __str__(self):
        return f"OrderItem {str(self.oid)} - Product {str(self.pid)}"


class Feedback(models.Model):
    """Model representing feedback on products by users."""
    uid = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    pid = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    cmt = models.TextField(
        blank=True,
        null=True,
        max_length=FIELD_MAX_LENGTH_XL,
        help_text=_("User comment about the product."),
    )
    rate = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("User rating of the product."),
    )

    def __str__(self):
        return f"Feedback by User {str(self.uid)} on Product {(self.pid)}"


def update_score_table(content_id, new_score, old_score):
    # Get or create the Score instance for the given content
    score_instance, created = Score.objects.get_or_create(cid=content_id)

    # Update the count for the new score
    if new_score:
        field_name = f'score{new_score}'
        current_count = getattr(score_instance, field_name)
        setattr(score_instance, field_name, current_count + 1)

    # Update the count for the old score if it exists
    if old_score:
        old_field_name = f'score{old_score}'
        old_current_count = getattr(score_instance, old_field_name)
        setattr(score_instance, old_field_name, old_current_count - 1)

    # Save the updated score instance
    score_instance.save()


def update_content_score(content_id):
    # Fetch the content instance
    content_instance = Content.objects.get(cid=content_id)

    # Fetch the associated score instance
    score_instance = Score.objects.get(cid=content)

    # Calculate the new score
    total_scores = sum([
        score_instance.score10 * 10,
        score_instance.score9 * 9,
        score_instance.score8 * 8,
        score_instance.score7 * 7,
        score_instance.score6 * 6,
        score_instance.score5 * 5,
        score_instance.score4 * 4,
        score_instance.score3 * 3,
        score_instance.score2 * 2,
        score_instance.score1 * 1
    ])

    total_votes = sum([
        score_instance.score10,
        score_instance.score9,
        score_instance.score8,
        score_instance.score7,
        score_instance.score6,
        score_instance.score5,
        score_instance.score4,
        score_instance.score3,
        score_instance.score2,
        score_instance.score1
    ])

    # Avoid division by zero
    if total_votes > 0:
        average_score = total_scores / total_votes
    else:
        average_score = 0

    # Update the Score_avg field in the Content model
    content_instance.scoreAvg = average_score
    content_instance.save(update_fields=['scoreAvg'])


def update_content_fav_sta(content_id, new_status, old_status):
    # Get or create the Score instance for the given content
    content_instance, created = Content.objects.get_or_create(cid=content_id)

    Content_status = {
        1: "watching",
        2: "completed",
        3: "onHold",
        4: "dropped",
        5: "reWatching",
        6: "planToWatch",
    }

    # Update the count for the new score
    if new_status:
        field_name = f'{Content_status[new_status]}'
        current_count = getattr(content_instance, field_name)
        setattr(content_instance, field_name, current_count + 1)
        fav_count = getattr(content_instance, "favorites")
        setattr(content_instance, field_name, fav_count + 1)

    # Update the count for the old score if it exists
    if old_status:
        old_field_name = f'{Content_status[old_status]}'
        old_current_count = getattr(content_instance, old_field_name)
        setattr(content_instance, old_field_name, old_current_count - 1)
        fav_count = getattr(content_instance, "favorites")
<<<<<<< HEAD
        setattr(content_instance, field_name, fav_count - 1)
=======
        setattr(content_instance, field_name, fav_count - 1)
>>>>>>> 815b201 (Create registration page)
