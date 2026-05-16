# init_db.py - Place in First_Module folder (same level as pathology_processor)
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pathology_processor.models.database import db_manager
from pathology_processor.services.seed_data import seed_database

def init_database():
    print("="*60)
    print("🔧 Initializing Pathology Database")
    print("="*60)
    
    base_dir = Path(__file__).parent
    db_path = base_dir / "pathology.db"
    print(f"📁 Database: {db_path}")
    
    # Create tables
    print("\n📊 Creating tables...")
    db_manager.create_tables()
    print("   ✅ Tables created")
    
    # Seed data
    print("\n🌱 Seeding data...")
    seed_database()
    print("   ✅ Seed data loaded")
    
    # Verify
    print("\n🔍 Verifying...")
    from pathology_processor.models.orm_models import CanonicalTest, TestAlias
    with db_manager.get_session() as session:
        test_count = session.query(CanonicalTest).count()
        alias_count = session.query(TestAlias).count()
        print(f"   ✅ Canonical tests: {test_count}")
        print(f"   ✅ Aliases: {alias_count}")
    
    print("\n" + "="*60)
    print("✅ Database initialization complete!")
    print("="*60)

if __name__ == "__main__":
    init_database()