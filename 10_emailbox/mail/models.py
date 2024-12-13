from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Email(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails") # 
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent") # Prevent deletion of the referenced object by raising "ProtectedError".
    recipients = models.ManyToManyField("User", related_name="emails_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [recipient.email for recipient in self.recipients.all()], # Note that one mail can be sent to multiple people.
            # Here we don't set a username for the user (instead we set a email as the username), so use email to represent the user. That's why "user.email" is used.
            # Note that each element in "self.recipients.all()" is a User class object.
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            # ".strftime(<format>)" converts date and time objects to their string representation, 
            # where <format> consists of various format codes that define specific parts of the date and time.
            # The format code we use here as below:
            # %b: Abbreviated month name, ex: Jan, Feb,…., Dec.
            # %d: Day of the month as a zero added decimal, ex: 01, 02,…., 31.
            # %Y: Year with century as a decimal number, ex: 2013, 2019 etc.
            # %I: Hour (12-hour clock) as a zero added decimal number, ex: 01, 02,…, 12.
            # %M: Minute as a zero added decimal number, ex: 00, 01,…., 59.
            # %p: Locale's AM or PM.
            # For example:
            #   datetime.now()                                      # 2024-04-16 16:46:34.444601  
            #   datetime.now().strftime("%b %d %Y, %I:%M %p")       # Apr 16 2024, 04:46 PM
            "read": self.read,
            "archived": self.archived
        }
