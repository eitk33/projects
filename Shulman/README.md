# Shul-man
#### Video Demo:  https://youtu.be/hiSecTItHq4
#### Description:
in Jewish orthodox laws we prey in the Shul 3 times a day, and with another 9 men (Minyan).
where I live, we are a small community and there are many struggles to make the Minyan. It requires someone that will send polls daily and manually, to make sure everyone saw the poll and\or the conformation etc.
.
In order to ease the effort of arranging the Minyan on every day, the Shul-man web app was created.

this app can accept the registering of new users as well as new communities and to help them getting their Minyan much more easily.

the Gabay (the guy responsible for the Shul's management) can send via email poll for whenever the Minyan will take place (and for which type of prayer Mincha, Arvit or Shabat).
users will get the e-mails with the link to enter the poll and the option to fill it.

all of the community member that will enter the app will be able to see the progress towards the Minyan (as well as to remove their on participation), and the Gabay can send conformation mail at the end in order to acknowledge all of the community members that there will be a Minyan.

Some features included:
1) registration:
    A) users will not be able to register with already taken username
    B) users will not be able to register if not providing format - applicable mail address

2) session:
    users will be logged in regularly to save the need to reconnect all the time

3) Preferences:
    A) users can choose whether they want to receive mails regarding poll for Minyan or conformation of Minyan that will take place
    B) users can register their role in the community (e.g., if they are the gabay).

4) Gabay:
    A) can send mails with the hour of the Minyan for the poll/conformation
    B) mails will be sent composed with sections and only once per click of the gabay, even if the gabay marked a few options (DB is taking care of this)

5) Poll:
    A) users will be able to mark attendance only for the prayers their Gabay sent
    B) users will not be able to mark (by mistake or not) attendance more than once per each prayer
    C) Users will be able to mark attendance more than once per each prayer in case they deregister themselves from that prayer


I had many indecisions I had to determine. some (but not all) of them were:

1) what will be the delivery system? should it be what's-app? SMS? web notifications?
    I decided to leave it with mail notifications for mainly two reasons: the lack of knowledge to establish the mentioned
    possibilities (I did try to handle with this, but it was a real time consuming), the desire for the app to remain completely free.

2) how to make sure that the app remains well targeted.
    this app was developed for my own community, but I wanted the enable others to use it as well.
    in order to do so I had to make sure that I established the correct structure of the DB so:
        A) Users will get their community info, nothing less and nothing more.
        B) Users will be able to replay to their community only in the manner needed so that their will not be any faults.

3) How can I get the app as much as user-friendly as possible in a limited time?
    This app (by its nature) requires a daily contact (Minyans are 3 times a day on every day)
    some ideas I had (whether neglected or not)
        A) automatic messaging - neglected. for this kind of feature, I had to implement constant time check and I saw it will take me to much time. In addition, prayers are depended by sunset. As a result, there will be probably law gain in this kind of feature
        B) keep users logged in so that they will not need to reconnect 3 times a day
        C) allowing users to deregister themselves and making sure that the rest of the community will be able to see it
