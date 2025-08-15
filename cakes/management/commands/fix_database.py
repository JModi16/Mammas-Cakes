from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix database schema by adding missing price column'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        try:
            # Check if price column exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='cakes_cake' AND column_name='price';
            """)
            result = cursor.fetchone()
            
            if not result:
                # Add the missing price column
                cursor.execute("ALTER TABLE cakes_cake ADD COLUMN price DECIMAL(8,2);")
                self.stdout.write(self.style.SUCCESS('✅ Price column added successfully!'))
            else:
                self.stdout.write(self.style.WARNING('⚠️ Price column already exists'))
            
            # Show all columns
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name='cakes_cake';
            """)
            columns = cursor.fetchall()
            
            self.stdout.write('\n📋 Current columns in cakes_cake table:')
            for col in columns:
                self.stdout.write(f'  • {col[0]} ({col[1]})')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))