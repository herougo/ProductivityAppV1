from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from productivity_core.models import WorkflowState


class Command(BaseCommand):
    help = 'Create default workflow states (Backlog, In Progress, Done) for users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            action='append',
            dest='user_ids',
            help='Target specific user IDs (can be specified multiple times)',
        )

    def handle(self, *args, **options):
        user_ids = options.get('user_ids')

        # Determine target users
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            if users.count() != len(user_ids):
                found_ids = set(users.values_list('id', flat=True))
                missing_ids = set(user_ids) - found_ids
                for missing_id in missing_ids:
                    self.stderr.write(
                        self.style.ERROR(f'✗ User with ID {missing_id} does not exist')
                    )
        else:
            # Get all users who don't have workflow states
            users = User.objects.filter(workflowstate__isnull=True).distinct()

        # Process each user
        created_count = 0
        skipped_count = 0
        error_count = 0

        for user in users:
            if self.user_has_workflow_states(user):
                self.stdout.write(
                    self.style.WARNING(
                        f'- User {user.id} ({user.username}) already has workflow states'
                    )
                )
                skipped_count += 1
                continue

            try:
                self.create_default_workflow_states(user)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created default workflow states for user {user.id} ({user.username})'
                    )
                )
                created_count += 1
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(
                        f'✗ Error processing user {user.id}: {str(e)}'
                    )
                )
                error_count += 1

        # Print summary
        total = created_count + skipped_count + error_count
        self.stdout.write(
            self.style.SUCCESS(
                f'\nProcessed {total} users: {created_count} created, '
                f'{skipped_count} skipped, {error_count} errors'
            )
        )

    def create_default_workflow_states(self, user):
        """Create the three default workflow states for a user."""
        default_states = [
            WorkflowState(
                user=user,
                order=1,
                name='backlog',
                display_name='Backlog',
                is_on_board=False,
                is_final=False,
            ),
            WorkflowState(
                user=user,
                order=2,
                name='in_progress',
                display_name='In Progress',
                is_on_board=True,
                is_final=False,
            ),
            WorkflowState(
                user=user,
                order=3,
                name='done',
                display_name='Done',
                is_on_board=True,
                is_final=True,
            ),
        ]

        with transaction.atomic():
            WorkflowState.objects.bulk_create(default_states)

    def user_has_workflow_states(self, user):
        """Check if user already has any workflow states."""
        return WorkflowState.objects.filter(user=user).exists()
