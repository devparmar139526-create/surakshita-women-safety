import sqlite3

def upgrade_database():
    """Add admin role support to existing database"""
    conn = sqlite3.connect('surakshita.db')
    cursor = conn.cursor()
    
    print("🔧 Starting database upgrade for security enhancements...")
    
    # Add is_admin column to users table
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0')
        print("✅ Added is_admin column to users table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("ℹ️  is_admin column already exists")
        else:
            raise
    
    # Prompt to create first admin user
    print("\n👤 Admin User Setup")
    create_admin = input("Do you want to grant admin privileges to an existing user? (y/n): ").lower()
    
    if create_admin == 'y':
        # Show existing users
        users = cursor.execute('SELECT id, username, email FROM users').fetchall()
        
        if not users:
            print("⚠️  No users found in database. Please register an account first.")
        else:
            print("\nExisting users:")
            for idx, user in enumerate(users, 1):
                print(f"  {idx}. {user[1]} ({user[2]})")
            
            try:
                choice = int(input(f"\nSelect user number to make admin (1-{len(users)}): "))
                if 1 <= choice <= len(users):
                    selected_user = users[choice - 1]
                    
                    cursor.execute('''
                        UPDATE users 
                        SET is_admin = 1 
                        WHERE id = ?
                    ''', (selected_user[0],))
                    
                    conn.commit()
                    print(f"✅ Granted admin privileges to {selected_user[1]}")
                else:
                    print("❌ Invalid selection")
            except (ValueError, IndexError):
                print("❌ Invalid input")
    
    conn.close()
    print("\n✅ Database upgrade complete!")
    print("\nℹ️  Next steps:")
    print("   1. Update app.py with admin_required decorator")
    print("   2. Protect admin routes")
    print("   3. Test admin access")

if __name__ == '__main__':
    upgrade_database()
