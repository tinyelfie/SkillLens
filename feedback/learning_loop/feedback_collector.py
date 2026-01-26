def collect_feedback():
    """
    Replace this with UI / API input later
    """
    print("\nDid the user accept the optimized resume?")
    accepted = input("Enter yes / no: ").strip().lower()

    return {
        "accepted": accepted == "yes"
    }
