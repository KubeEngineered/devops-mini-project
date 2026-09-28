from datetime import datetime, timedelta, timezone

DAYS_DELETION_LIMIT = 180


def get_deletion_cutoff_timestamp():
    """Returns UTC datetime object representing the 180-day cutoff threshold."""
    return datetime.now(timezone.utc) - timedelta(days=DAYS_DELETION_LIMIT)


def auto_delete_expired_accounts(db_session):
    """Permanently deletes or soft-deletes users inactive for > 180 days."""
    cutoff_date = get_deletion_cutoff_timestamp()

    # Query active OR deactivated users whose last_active_at is older than 180 days
    expired_users = (
        db_session.query(User)
        .filter(User.last_active_at < cutoff_date)
        .all()
    )

    deleted_count = 0
    for user in expired_users:
        # Step A: Anonymize or clean up user's personal health/fitness metrics if required
        # (e.g., delete activity logs, workout histories, synced health kit data)
        cleanup_user_related_data(user.id, db_session)

        # Step B: Remove the user record from the database
        db_session.delete(user)
        deleted_count += 1

    db_session.commit()
    print(f"[{datetime.now(timezone.utc)}] Successfully deleted {deleted_count} accounts inactive for > 180 days.")
    return deleted_count


def cleanup_user_related_data(user_id, db_session):
    """Helper to clean up foreign key relationships or sensitive personal data."""
    # Example ORM query for related records:
    # db_session.query(WorkoutLog).filter(WorkoutLog.user_id == user_id).delete()
    pass
