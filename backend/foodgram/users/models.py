from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import OuterRef, Exists, Count


class UserQuerySet(models.QuerySet):
    def add_anotations_user(self, user_id):
        return User.objects.all(
            ).annotate(
            is_subscribed=Exists(
                Follow.objects.filter(
                    user_id=user_id, author__id=OuterRef('id')))
                    ).annotate(recipes_limit=Count('recipe'))


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    )

    email = models.EmailField(
        verbose_name='Почта', max_length=254, unique=True)
    username = models.CharField(
        'Никнэйм', max_length=150, unique=True
    )
    first_name = models.CharField(
        'Имя', max_length=150,
    )
    last_name = models.CharField(
        'Фамилия', max_length=150
    )
    password = models.CharField(
        'Пароль', max_length=150
    )

    # role = models.CharField(
    #    'Роль',
    #    max_length=max([len(role) for role, name in ROLES]),
    #    choices=ROLES, default=USER
    # )

    # @property
    # def is_admin(self):
    #    return self.role == self.ADMIN or self.is_superuser or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    objects = UserQuerySet.as_manager()

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name_plural = "Подписки"
        constraints = (models.UniqueConstraint(
            fields=['user', 'author'], name='unique_combination'),)
