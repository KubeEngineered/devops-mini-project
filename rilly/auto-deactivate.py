from datetime import datetime, timedelta, timezone

# Cutoff threshold: 45 days ago from right now
DAYS_INACTIVE_LIMIT = 45


def get_cutoff_timestamp():
    """Returns UTC datetime object representing the cutoff threshold."""
    return datetime.now(timezone.utc) - timedelta(days=DAYS_INACTIVE_LIMIT)


def auto_deactivate_inactive_users(db_session):
    """Queries for active users inactive for > 45 days and deactivates them."""
    cutoff_date = get_cutoff_timestamp()

    # Generic ORM Query Example (e.g., SQLAlchemy)
    # Find active users whose last_active date is strictly before the cutoff
    inactive_users = (
        db_session.query(User)
        .filter(User.is_active == True)
        .filter(User.last_active_at < cutoff_date)
        .all()
    )

    deactivated_count = 0
    for user in inactive_users:
        user.is_active = False
        user.deactivated_at = datetime.now(timezone.utc)
        user.deactivation_reason = "auto_inactivity_45_days"
        deactivated_count += 1

    db_session.commit()
    print(f"[{datetime.now(timezone.utc)}] Successfully deactivated {deactivated_count} users.")
    return deactivated_count
