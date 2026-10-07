class AccountUpdateError(Exception):
    """Custom exception raised when a user attempts to modify restricted account fields."""
    pass


class RillyUserProfile:
    def __init__(self, user_id: str, email: str, phone: str, name: str):
        # Immutable core identity fields
        self.user_id = user_id
        self._email = email
        self._phone = phone
        
        # Account status & editable profile attributes
        self.is_account_setup_complete = False
        self.name = name

    @property
    def email(self) -> str:
        """Getter for email address."""
        return self._email

    @email.setter
    def email(self, new_email: str):
        """Setter that blocks modifications once account setup is complete."""
        if self.is_account_setup_complete:
            raise AccountUpdateError(
                "Rilly Security Policy: Email address cannot be modified after account setup."
            )
        self._email = new_email

    @property
    def phone(self) -> str:
        """Getter for phone number."""
        return self._phone

    @phone.setter
    def phone(self, new_phone: str):
        """Setter that blocks modifications once account setup is complete."""
        if self.is_account_setup_complete:
            raise AccountUpdateError(
                "Rilly Security Policy: Phone number cannot be modified after account setup."
            )
        self._phone = new_phone

    def complete_setup(self):
        """Marks initial onboarding and account setup as complete."""
        self.is_account_setup_complete = True
        print("✓ Account setup completed successfully. Core identity fields are now locked.")


# --- Demo / Testing the Logic ---
if __name__ == "__main__":
    # 1. User registers initial details
    user = RillyUserProfile(
        user_id="usr_10293",
        email="aditya@example.com",
        phone="+919876543210",
        name="Aditya"
    )

    # 2. Modifying email/phone BEFORE setup completes (Allowed)
    user.email = "aditya.updated@example.com"
    print(f"Pre-setup email updated to: {user.email}")

    # 3. Finalize setup process
    user.complete_setup()

    # 4. Attempting to update allowed fields (Name) - Allowed
    user.name = "Aditya G."
    print(f"Name updated successfully to: {user.name}")

    # 5. Attempting to update Email AFTER setup completes - Blocked
    try:
        user.email = "new.email@example.com"
    except AccountUpdateError as e:
        print(f"❌ Blocked: {e}")

    # 6. Attempting to update Phone AFTER setup completes - Blocked
    try:
        user.phone = "+919999988888"
    except AccountUpdateError as e:
        print(f"❌ Blocked: {e}")
