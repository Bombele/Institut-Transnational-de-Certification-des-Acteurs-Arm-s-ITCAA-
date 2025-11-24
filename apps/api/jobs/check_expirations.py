# apps/api/jobs/check_expirations.py
from apps.api.database import SessionLocal, init_db
from apps.api.services.tracking_service import check_expiring_mous, check_expiring_mandates

def run():
    init_db()
    db = SessionLocal()
    mous = check_expiring_mous(db)
    mandates = check_expiring_mandates(db)
    if mous or mandates:
        print("⚠️ Alertes ITCAA :")
        for m in mous:
            print(f"MoU avec {m.partner_name} expire le {m.expires_at}")
        for md in mandates:
            print(f"Mandat du membre {md.member_id} expire le {md.end_date}")
    else:
        print("✅ Aucun MoU ou mandat proche de l’expiration.")

if __name__ == "__main__":
    run()
