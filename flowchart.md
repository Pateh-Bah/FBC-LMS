# FBC Library Management System - Simplified Mermaid Flowchart

## System Architecture Overview

```mermaid
flowchart TB
    %% Authentication Layer
    A[User Login] --> B{Authentication Check}
    B -->|Valid| C{Role Verification}
    B -->|Invalid| A
    
    %% Role Routing
    C -->|Admin| D[Admin Dashboard]
    C -->|Staff| E[Staff Dashboard]  
    C -->|Lecturer| F[Lecturer Dashboard]
    C -->|Student| G{Subscription Check}
    
    %% Student Flow
    G -->|Active| H[Student Dashboard]
    G -->|Expired| I[Payment Required]
    I --> J[Payment Process]
    J --> H
    
    %% Admin Features
    D --> D1[User Management]
    D --> D2[Book Management]
    D --> D3[System Settings]
    D --> D4[Reports]
    
    %% Staff Features  
    E --> E1[Limited User Mgmt]
    E --> E2[Book Operations]
    E --> E3[Fine Management]
    E --> E4[Payment Verification]
    
    %% Lecturer Features
    F --> F1[Browse Books]
    F --> F2[Borrow Requests]
    F --> F3[View History]
    F --> F4[Pay Fines]
    
    %% Student Features
    H --> H1[Browse Catalog]
    H --> H2[E-Book Reading]
    H --> H3[Subscription Mgmt]
    H --> H4[Payment History]
```

## User Journey Flowchart

```mermaid
flowchart TD
    %% User Entry Point
    START([User Visits System]) --> LOGIN[Login Page]
    LOGIN --> AUTH{Authentication}
    AUTH -->|Success| ROLE{Role Check}
    AUTH -->|Failure| LOGIN

    %% Role-based Routing
    ROLE -->|Admin| ADMIN_DASH[Admin Dashboard]
    ROLE -->|Staff| STAFF_DASH[Staff Dashboard]
    ROLE -->|Lecturer| LECTURER_DASH[Lecturer Dashboard]
    ROLE -->|Student| SUB_CHECK{Subscription Active?}

    %% Student Subscription Flow
    SUB_CHECK -->|Yes| STUDENT_DASH[Student Dashboard]
    SUB_CHECK -->|No| SUB_REQUIRED[Subscription Required]
    SUB_REQUIRED --> PAYMENT_FLOW[Payment Process]
    PAYMENT_FLOW --> SUB_SUCCESS{Payment Success?}
    SUB_SUCCESS -->|Yes| STUDENT_DASH
    SUB_SUCCESS -->|No| SUB_REQUIRED

    %% Admin User Journey
    ADMIN_DASH --> ADMIN_ACTIONS{Admin Actions}
    ADMIN_ACTIONS -->|User Management| USER_CRUD[Create/Edit/Delete Users]
    ADMIN_ACTIONS -->|Book Management| BOOK_CRUD[Manage Books & E-books]
    ADMIN_ACTIONS -->|System Config| SYS_CONFIG[Configure System Settings]
    ADMIN_ACTIONS -->|Reports| REPORTS[Generate Reports]
    ADMIN_ACTIONS -->|Verify Payments| PAY_VERIFY[Payment Verification]

    %% Staff User Journey
    STAFF_DASH --> STAFF_ACTIONS{Staff Actions}
    STAFF_ACTIONS -->|Process Returns| RETURN_PROCESS[Book Return Processing]
    STAFF_ACTIONS -->|Approve Requests| APPROVE_REQ[Approve Borrow Requests]
    STAFF_ACTIONS -->|Manage Fines| FINE_MGT[Fine Management]
    STAFF_ACTIONS -->|Limited User Mgmt| LIMITED_USER[Manage Students/Lecturers]

    %% Lecturer User Journey
    LECTURER_DASH --> LEC_ACTIONS{Lecturer Actions}
    LEC_ACTIONS -->|Browse Books| BROWSE_BOOKS[Browse Book Catalog]
    LEC_ACTIONS -->|Read E-books| READ_EBOOK[Online E-book Reading]
    LEC_ACTIONS -->|Borrow Request| BORROW_REQ[Submit Borrow Request]
    LEC_ACTIONS -->|Pay Fines| PAY_FINE[Fine Payment Process]
    LEC_ACTIONS -->|View History| VIEW_HISTORY[Borrowing History]

    %% Student User Journey
    STUDENT_DASH --> STU_ACTIONS{Student Actions}
    STU_ACTIONS -->|Browse Books| BROWSE_BOOKS
    STU_ACTIONS -->|Read E-books| READ_EBOOK
    STU_ACTIONS -->|Borrow Request| BORROW_REQ
    STU_ACTIONS -->|Pay Fines| PAY_FINE
    STU_ACTIONS -->|Manage Subscription| MANAGE_SUB[Subscription Management]
    STU_ACTIONS -->|Payment History| PAY_HISTORY[View Payment History]

    %% Borrow Request Process
    BORROW_REQ --> CHECK_STOCK{Book Available?}
    CHECK_STOCK -->|Yes| SUBMIT_REQ[Submit Request to Staff]
    CHECK_STOCK -->|No| STOCK_NOTIFY[Stock Unavailable Notice]
    
    SUBMIT_REQ --> STAFF_REVIEW{Staff Review}
    STAFF_REVIEW -->|Approved| ASSIGN_DUE[Assign Due Date]
    STAFF_REVIEW -->|Rejected| REJECT_NOTICE[Rejection Notice]
    
    ASSIGN_DUE --> BOOK_BORROWED[Book Status: Borrowed]
    BOOK_BORROWED --> DUE_REMINDER[Due Date Reminders]
    DUE_REMINDER --> RETURN_CHECK{Returned on Time?}
    RETURN_CHECK -->|Yes| RETURN_SUCCESS[Return Successful]
    RETURN_CHECK -->|No| CALCULATE_FINE[Calculate Overdue Fine]
    CALCULATE_FINE --> FINE_NOTIFY[Fine Notification]

    %% Payment Process Detail
    PAYMENT_FLOW --> SELECT_METHOD{Select Payment Method}
    SELECT_METHOD -->|Orange Money| ORANGE_FLOW[Phone + OTP Verification]
    SELECT_METHOD -->|Afrimoney| AFRI_FLOW[Phone + PIN Verification]
    SELECT_METHOD -->|QMoney| Q_FLOW[Account + PIN Verification]
    SELECT_METHOD -->|PayPal| PP_FLOW[Email + Password Simulation]
    SELECT_METHOD -->|Bank Transfer| BANK_FLOW[Account + Reference Number]

    ORANGE_FLOW --> PROCESS_PAYMENT[Process Transaction]
    AFRI_FLOW --> PROCESS_PAYMENT
    Q_FLOW --> PROCESS_PAYMENT
    PP_FLOW --> PROCESS_PAYMENT
    BANK_FLOW --> PROCESS_PAYMENT

    PROCESS_PAYMENT --> GENERATE_RECEIPT[Generate Receipt]
    GENERATE_RECEIPT --> ADMIN_VERIFY[Admin Verification Required]
    ADMIN_VERIFY --> PAYMENT_COMPLETE[Payment Complete]

    %% Return to Dashboard
    USER_CRUD --> ADMIN_DASH
    BOOK_CRUD --> ADMIN_DASH
    SYS_CONFIG --> ADMIN_DASH
    REPORTS --> ADMIN_DASH
    PAY_VERIFY --> ADMIN_DASH

    RETURN_PROCESS --> STAFF_DASH
    APPROVE_REQ --> STAFF_DASH
    FINE_MGT --> STAFF_DASH
    LIMITED_USER --> STAFF_DASH

    BROWSE_BOOKS --> LECTURER_DASH
    READ_EBOOK --> LECTURER_DASH
    VIEW_HISTORY --> LECTURER_DASH

    MANAGE_SUB --> STUDENT_DASH
    PAY_HISTORY --> STUDENT_DASH

    RETURN_SUCCESS --> LECTURER_DASH
    RETURN_SUCCESS --> STUDENT_DASH
    FINE_NOTIFY --> PAY_FINE
    PAYMENT_COMPLETE --> STUDENT_DASH

    %% Styling for User Journey
    classDef startEnd fill:#e17055,stroke:#d63031,stroke-width:3px,color:#fff
    classDef process fill:#74b9ff,stroke:#0984e3,stroke-width:2px,color:#fff
    classDef decision fill:#fdcb6e,stroke:#e84393,stroke-width:2px,color:#000
    classDef adminAction fill:#ff6b6b,stroke:#d63031,stroke-width:2px,color:#fff
    classDef staffAction fill:#4ecdc4,stroke:#00b894,stroke-width:2px,color:#fff
    classDef lecturerAction fill:#45b7d1,stroke:#0984e3,stroke-width:2px,color:#fff
    classDef studentAction fill:#96ceb4,stroke:#00b894,stroke-width:2px,color:#fff

    class START startEnd
    class AUTH,ROLE,SUB_CHECK,ADMIN_ACTIONS,STAFF_ACTIONS,LEC_ACTIONS,STU_ACTIONS,CHECK_STOCK,STAFF_REVIEW,RETURN_CHECK,SELECT_METHOD decision
    class LOGIN,PAYMENT_FLOW,BORROW_REQ,PROCESS_PAYMENT,GENERATE_RECEIPT process
    class ADMIN_DASH,USER_CRUD,BOOK_CRUD,SYS_CONFIG,REPORTS,PAY_VERIFY adminAction
    class STAFF_DASH,RETURN_PROCESS,APPROVE_REQ,FINE_MGT,LIMITED_USER staffAction
    class LECTURER_DASH,BROWSE_BOOKS,READ_EBOOK,VIEW_HISTORY lecturerAction
    class STUDENT_DASH,MANAGE_SUB,PAY_HISTORY studentAction
```

## System Data Flow

```mermaid
graph LR
    %% User Input Layer
    subgraph UI ["User Interface Layer"]
        UI1[Admin Interface]
        UI2[Staff Interface] 
        UI3[Lecturer Interface]
        UI4[Student Interface]
    end

    %% Business Logic Layer
    subgraph BL ["Business Logic Layer"]
        BL1[Authentication Service]
        BL2[User Management Service]
        BL3[Book Management Service]
        BL4[Borrowing Service]
        BL5[Fine Management Service]
        BL6[Payment Service]
        BL7[Notification Service]
    end

    %% Data Access Layer
    subgraph DA ["Data Access Layer"]
        DA1[User Repository]
        DA2[Book Repository]
        DA3[Borrowing Repository]
        DA4[Fine Repository]
        DA5[Payment Repository]
        DA6[Notification Repository]
        DA7[System Settings Repository]
    end

    %% Database Layer
    subgraph DB_LAYER ["Database"]
        DB1[(Users)]
        DB2[(Books)]
        DB3[(E-Books)]
        DB4[(Borrowings)]
        DB5[(Fines)]
        DB6[(Payments)]
        DB7[(Notifications)]
        DB8[(System Settings)]
    end

    %% External Services
    subgraph EXT ["External Services"]
        EXT1[Email Service]
        EXT2[File Storage]
        EXT3[Payment Gateways]
    end

    %% Data Flow Connections
    UI1 --> BL1
    UI1 --> BL2
    UI1 --> BL3
    UI1 --> BL5
    UI1 --> BL6
    UI1 --> BL7

    UI2 --> BL1
    UI2 --> BL2
    UI2 --> BL3
    UI2 --> BL4
    UI2 --> BL5
    UI2 --> BL6

    UI3 --> BL1
    UI3 --> BL3
    UI3 --> BL4
    UI3 --> BL5
    UI3 --> BL6

    UI4 --> BL1
    UI4 --> BL3
    UI4 --> BL4
    UI4 --> BL5
    UI4 --> BL6

    BL1 --> DA1
    BL2 --> DA1
    BL3 --> DA2
    BL4 --> DA3
    BL5 --> DA4
    BL6 --> DA5
    BL7 --> DA6

    DA1 --> DB1
    DA2 --> DB2
    DA2 --> DB3
    DA3 --> DB4
    DA4 --> DB5
    DA5 --> DB6
    DA6 --> DB7
    DA7 --> DB8

    BL6 --> EXT3
    BL7 --> EXT1
    BL3 --> EXT2

    %% Styling
    classDef uiLayer fill:#81ecec,stroke:#00cec9,stroke-width:2px,color:#000
    classDef businessLayer fill:#fab1a0,stroke:#e17055,stroke-width:2px,color:#000
    classDef dataLayer fill:#fd79a8,stroke:#e84393,stroke-width:2px,color:#fff
    classDef dbLayer fill:#a29bfe,stroke:#6c5ce7,stroke-width:2px,color:#fff
    classDef extLayer fill:#55a3ff,stroke:#2d3436,stroke-width:2px,color:#fff

    class UI1,UI2,UI3,UI4 uiLayer
    class BL1,BL2,BL3,BL4,BL5,BL6,BL7 businessLayer
    class DA1,DA2,DA3,DA4,DA5,DA6,DA7 dataLayer
    class DB1,DB2,DB3,DB4,DB5,DB6,DB7,DB8 dbLayer
    class EXT1,EXT2,EXT3 extLayer
```

## Payment System Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant P as Payment Gateway
    participant A as Admin
    participant D as Database

    Note over U,D: Payment Process Flow

    U->>S: Initiate Payment
    S->>U: Display Payment Methods
    U->>S: Select Payment Method
    
    alt Orange Money
        U->>S: Enter Phone Number
        S->>P: Validate Phone Number
        P-->>S: Send OTP
        S->>U: Request OTP
        U->>S: Enter OTP
        S->>P: Verify OTP
    
    else Afrimoney
        U->>S: Enter Phone & PIN
        S->>P: Validate Credentials
        P-->>S: Validation Result
    
    else QMoney
        U->>S: Enter Account & PIN
        S->>P: Validate Account
        P-->>S: Account Status
    
    else PayPal
        U->>S: Enter Email & Password
        S->>P: Simulate PayPal Login
        P-->>S: Login Status
    
    else Bank Transfer
        U->>S: Select Bank & Enter Details
        S->>P: Validate Account
        P-->>S: Account Verification
    end

    P-->>S: Payment Processing
    S->>D: Save Transaction Record
    S->>U: Generate Receipt
    S->>A: Send for Admin Verification
    
    A->>S: Review Transaction
    A->>S: Approve/Reject Payment
    S->>D: Update Payment Status
    S->>U: Payment Confirmation
    
    Note over U,D: Payment Complete
```

## Enhanced ER Diagram for FBC Library Management System

```mermaid
erDiagram
    USER ||--o{ BORROW : "has"
    USER ||--o{ FINE : "penalized"
    USER ||--o{ PAYMENT : "makes"
    USER {
        int id
        string name
        string email
        string phone
        string role
        date date_joined
        bool is_active
    }

    BOOK ||--o{ BORROW : "includes"
    BOOK ||--o{ FINE : "involves"
    BOOK {
        int id
        string title
        string author
        string category
        int total_copies
        int available_copies
        date published_date
    }

    BORROW {
        int id
        date borrow_date
        date return_date
        string status
        int renewal_count
    }

    FINE {
        int id
        decimal amount
        string reason
        date date_issued
        bool is_paid
    }

    PAYMENT {
        int id
        string method
        decimal amount
        date payment_date
        string payment_type
        string transaction_id
    }

    NOTIFICATION {
        int id
        string message
        date sent_date
        bool is_read
    }

    USER ||--o{ NOTIFICATION : "receives"
    BORROW ||--o{ NOTIFICATION : "triggers"
    FINE ||--o{ NOTIFICATION : "alerts"
    PAYMENT ||--o{ NOTIFICATION : "confirms"
```

This documentation provides a simplified version of the FBC Library Management System flowcharts, focusing on key components and user journeys for easier understanding and compatibility with various rendering tools.
