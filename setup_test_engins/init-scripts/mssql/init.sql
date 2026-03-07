-- MSSQL Dummy Data: CRM System
-- Create database
IF NOT EXISTS (
    SELECT name
    FROM sys.databases
    WHERE
        name = 'crm_db'
)
CREATE DATABASE crm_db;
GO

USE crm_db;
GO

-- Contacts table
CREATE TABLE contacts (
    id INT IDENTITY (1, 1) PRIMARY KEY,
    full_name NVARCHAR (150) NOT NULL,
    email NVARCHAR (150) UNIQUE,
    phone NVARCHAR (30),
    company NVARCHAR (150),
    created_at DATETIME2 DEFAULT GETDATE ()
);
GO

-- Deals table
CREATE TABLE deals (
    id INT IDENTITY (1, 1) PRIMARY KEY,
    contact_id INT FOREIGN KEY REFERENCES contacts (id),
    title NVARCHAR (200),
    value DECIMAL(12, 2),
    stage NVARCHAR (50) DEFAULT 'Lead',
    close_date DATE,
    created_at DATETIME2 DEFAULT GETDATE ()
);
GO

-- Activities table
CREATE TABLE activities (
    id INT IDENTITY (1, 1) PRIMARY KEY,
    deal_id INT FOREIGN KEY REFERENCES deals (id),
    type NVARCHAR (50), -- Call, Email, Meeting
    notes NVARCHAR (MAX),
    activity_at DATETIME2 DEFAULT GETDATE ()
);
GO

-- Dummy Contacts
INSERT INTO
    contacts (
        full_name,
        email,
        phone,
        company
    )
VALUES (
        N'Ahmed Al-Rashid',
        'ahmed@corp.sa',
        '+966501234567',
        'Saudi Tech Co'
    ),
    (
        N'Emily Watson',
        'emily@uk-firm.co',
        '+447911123456',
        'UK Consulting'
    ),
    (
        N'Tariq Nasser',
        'tariq@gulf.ae',
        '+971521234567',
        'Gulf Industries'
    ),
    (
        N'Maria Santos',
        'maria@br.com',
        '+5511999887766',
        'Santos Group'
    ),
    (
        N'James O\'Brien',
        'james@us-inc.com',
        '+14155552671',
        'US Innovations'
    );
GO

-- Dummy Deals
INSERT INTO
    deals (
        contact_id,
        title,
        value,
        stage,
        close_date
    )
VALUES (
        1,
        'Enterprise License 2026',
        125000.00,
        'Negotiation',
        '2026-06-30'
    ),
    (
        2,
        'Consulting Package Q2',
        45000.00,
        'Proposal',
        '2026-04-15'
    ),
    (
        3,
        'Cloud Migration Project',
        280000.00,
        'Won',
        '2026-02-28'
    ),
    (
        4,
        'Support Contract Renewal',
        18000.00,
        'Lead',
        '2026-07-01'
    ),
    (
        5,
        'AI Integration POC',
        62000.00,
        'Demo',
        '2026-05-20'
    );
GO

-- Dummy Activities
INSERT INTO
    activities (deal_id, type, notes)
VALUES (
        1,
        'Call',
        N'Initial discovery call — strong interest in Enterprise tier'
    ),
    (
        1,
        'Email',
        N'Sent pricing proposal PDF'
    ),
    (
        2,
        'Meeting',
        N'Onsite presentation delivered, follow-up scheduled'
    ),
    (
        3,
        'Email',
        N'Contract signed and sent to legal'
    ),
    (
        4,
        'Call',
        N'Left voicemail, awaiting callback'
    ),
    (
        5,
        'Demo',
        N'Live demo of AI module — client impressed'
    );
GO

PRINT '✅ MSSQL: crm_db loaded with contacts, deals, activities';
GO