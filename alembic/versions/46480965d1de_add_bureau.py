"""Add bureau column and bureau data to agencies

Revision ID: 46480965d1de
Revises: cd2fe647faf7
Create Date: 2023-05-31 16:25:05.338022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46480965d1de'
down_revision = 'cd2fe647faf7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('agencies', sa.Column('bureau', sa.String(), nullable=True))
    op.execute("""
               ALTER TABLE agencies
               DROP CONSTRAINT IF EXISTS ix_agencies_name;
               """)
    op.execute("""
               DROP INDEX IF EXISTS ix_agencies_name;
               """)
    op.execute("""
               insert into agencies(name, bureau)
                values
                ('Department of Justice','Bureau of Alcohol, Tobacco, Firearms and Explosives (ATF)'),
                ('Department of Justice','Drug Enforcement Administration (DEA)'),
                ('Department of Justice','Federal Bureau of Prisons (BOP)'),
                ('Department of Justice','Federal Bureau of Investigation (FBI)'),
                ('Department of Justice','Federal Prison Industries (FPI)'),
                ('Department of Justice','Justice Management Division-Offices, Boards and Divisions (OBD)'),
                ('Department of Justice','Office of Justice Programs (OJP)'),
                ('Department of Justice','U.S. Marshals Service (USMS)'),
                ('Department of Justice','Other'),
                ('Department of the Treasury','Alcohol and Tobacco Tax and Trade Bureau'),
                ('Department of the Treasury','Bureau of the Fiscal Service'),
                ('Department of the Treasury','Bureau of Engraving and Printing'),
                ('Department of the Treasury','Community Development Financial Institutions Fund'),
                ('Department of the Treasury','Comptroller of the Currency'),
                ('Department of the Treasury','Financial Crimes Enforcement Network'),
                ('Department of the Treasury','Internal Revenue Service'),
                ('Department of the Treasury','Special Inspector General for the Troubled Asset Relief Program'),
                ('Department of the Treasury','Special Inspector General for Pandemic Recovery'),
                ('Department of the Treasury','Treasury Inspector General for Tax Administration'),
                ('Department of the Treasury','United States Mint'),
                ('Department of the Treasury','Other'),
                ('Department of Education','Departmental Management'),
                ('Department of Education','Disaster Education Recovery'),
                ('Department of Education','Institute of Education Sciences'),
                ('Department of Education','Office of Career, Technical, and Adult Education'),
                ('Department of Education','Office of Elementary and Secondary Education'),
                ('Department of Education','Office of English Language Acquisition'),
                ('Department of Education','Office of Federal Student Aid'),
                ('Department of Education','Office of Innovation and Improvement'),
                ('Department of Education','Office of Postsecondary Education'),
                ('Department of Education','Office of Special Education and Rehabilitative Services'),
                ('Department of Education','Other'),
                ('Department of Transportation','Federal Aviation Administration'),
                ('Department of Transportation','Federal Highway Administration'),
                ('Department of Transportation','Federal Motor Carrier Safety Administration'),
                ('Department of Transportation','Federal Railroad Administration'),
                ('Department of Transportation','Federal Transit Administration'),
                ('Department of Transportation','Great Lakes St. Lawrence Seaway Development Corporation'),
                ('Department of Transportation','Maritime Administration'),
                ('Department of Transportation','National Highway Traffic Safety Administration'),
                ('Department of Transportation','Office of Inspector General'),
                ('Department of Transportation','Office of the Secretary'),
                ('Department of Transportation','Pipeline and Hazardous Materials Safety Administration'),
                ('Department of Transportation','Transportation Safety Institute'),
                ('Department of Transportation','Volpe National Transportation Systems Center'),
                ('Department of Transportation','Working Capital Fund'),
                ('Department of Transportation','Other'),
                ('National Science Foundation','Directorate for Biological Sciences  (BIO/OAD)'),
                ('National Science Foundation','Directorate for Engineering  (ENG)'),
                ('National Science Foundation','Directorate for Mathematical & Physical Sciences  (MPS)'),
                ('National Science Foundation','Directorate for Social, Behavioral & Economic Sciences  (SBE)'),
                ('National Science Foundation','Directorate for STEM Education  (EDU)'),
                ('National Science Foundation','Directorate for Technology, Innovation and Partnerships  (TIP)'),
                ('National Science Foundation','Division of Computer and Network Systems  (CISE)'),
                ('National Science Foundation','National Science Board  (NSB)'),
                ('National Science Foundation','Office of Budget, Finance, and Award Management  (BFA)'),
                ('National Science Foundation','Office of General Council (OGC)'),
                ('National Science Foundation','Office of Information & Resource Management  (OIRM)'),
                ('National Science Foundation','Office of Inspector General  (OIG)'),
                ('National Science Foundation','Office of the Director  (OD)'),
                ('National Science Foundation','Other'),
                ('General Services Administration','Federal Acquisition Service'),
                ('General Services Administration','Public Buildings Service'),
                ('General Services Administration','Office of Administrative Services'),
                ('General Services Administration','Office of Civil Rights'),
                ('General Services Administration','Office of Congressional & Intergovernmental Affairs'),
                ('General Services Administration','Office of Customer Experience'),
                ('General Services Administration','Office of General Counsel'),
                ('General Services Administration','Office of Government-wide Policy'),
                ('General Services Administration','Office of Human Resource Management'),
                ('General Services Administration','Office of Mission Assurance'),
                ('General Services Administration','Office of Small and Disadvantaged Business Utilization'),
                ('General Services Administration','Office Strategic Communication'),
                ('General Services Administration','Office of the Chief Information Officer (GSA IT)'),
                ('General Services Administration','Office of the Chief Financial Officer')

               """)


def downgrade() -> None:
    op.execute("""
               delete from agencies
               where name in ('Department of Justice','Department of the Treasury','Department of Education','Department of Transportation',
               'National Science Foundation','General Services Administration') and bureau is not null
               """)
    op.drop_column('agencies', 'bureau')
    op.create_index(op.f('ix_agencies_name'), 'agencies', ['name'], unique=True)
