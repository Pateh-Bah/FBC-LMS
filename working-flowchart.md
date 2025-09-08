# FBC Library Management System - Working Mermaid Flowcharts

## 1. System Architecture Overview

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
    
    %% Styling
    classDef admin fill:#ff6b6b
    classDef staff fill:#4ecdc4
    classDef lecturer fill:#45b7d1
    classDef student fill:#96ceb4
    
    class D,D1,D2,D3,D4 admin
    class E,E1,E2,E3,E4 staff
    class F,F1,F2,F3,F4 lecturer
    class H,H1,H2,H3,H4 student
```

## 2. User Journey Flow

```mermaid
flowchart TD
    START([User Visits System]) --> LOGIN[Login Page]
    LOGIN --> AUTH{Valid Credentials?}
    
    AUTH -->|No| LOGIN
    AUTH -->|Yes| ROLE{User Role}
    
    ROLE -->|Admin| ADMIN[Admin Dashboard]
    ROLE -->|Staff| STAFF[Staff Dashboard]
    ROLE -->|Lecturer| LEC[Lecturer Dashboard]
    ROLE -->|Student| SUB{Has Subscription?}
    
    SUB -->|Yes| STUDENT[Student Dashboard]
    SUB -->|No| PAY[Payment Portal]
    PAY --> PAYMENT[Process Payment]
    PAYMENT --> STUDENT
    
    %% Admin Actions
    ADMIN --> A1[Manage Users]
    ADMIN --> A2[Manage Books]
    ADMIN --> A3[System Config]
    
    %% Staff Actions
    STAFF --> S1[Process Returns]
    STAFF --> S2[Approve Requests]
    STAFF --> S3[Manage Fines]
    
    %% Lecturer Actions
    LEC --> L1[Browse Books]
    LEC --> L2[Submit Requests]
    LEC --> L3[Pay Fines]
    
    %% Student Actions
    STUDENT --> ST1[Browse Catalog]
    STUDENT --> ST2[Read E-books]
    STUDENT --> ST3[Manage Subscription]
```

## 3. Book Borrowing Process

```mermaid
flowchart TD
    USER[User Submits Borrow Request] --> CHECK{Book Available?}
    
    CHECK -->|No| DENY[Request Denied]
    CHECK -->|Yes| SUBMIT[Request Submitted]
    
    SUBMIT --> REVIEW{Staff Review}
    REVIEW -->|Reject| REJECT[Request Rejected]
    REVIEW -->|Approve| APPROVE[Request Approved]
    
    APPROVE --> ASSIGN[Assign Due Date]
    ASSIGN --> BORROWED[Book Status: Borrowed]
    
    BORROWED --> DUE[Due Date Approaches]
    DUE --> REMIND[Send Reminder]
    
    REMIND --> RETURN{Book Returned?}
    RETURN -->|On Time| SUCCESS[Return Successful]
    RETURN -->|Late| FINE[Calculate Fine]
    
    FINE --> NOTIFY[Send Fine Notice]
    NOTIFY --> PAYMENT[Payment Required]
    PAYMENT --> SUCCESS
```

## 4. Payment Processing Flow

```mermaid
flowchart TD
    INITIATE[User Initiates Payment] --> SELECT{Select Payment Method}
    
    SELECT -->|Orange Money| ORANGE[Phone + OTP]
    SELECT -->|Afrimoney| AFRI[Phone + PIN]
    SELECT -->|QMoney| QMONEY[Account + PIN]
    SELECT -->|PayPal| PAYPAL[Email + Password]
    SELECT -->|Bank Transfer| BANK[Account + Reference]
    
    ORANGE --> PROCESS[Process Transaction]
    AFRI --> PROCESS
    QMONEY --> PROCESS
    PAYPAL --> PROCESS
    BANK --> PROCESS
    
    PROCESS --> RECEIPT[Generate Receipt]
    RECEIPT --> VERIFY[Admin Verification]
    VERIFY --> COMPLETE[Payment Complete]
```

## 5. System Data Flow

```mermaid
flowchart LR
    UI[User Interface] --> BL[Business Logic]
    BL --> DA[Data Access Layer]
    DA --> DB[(Database)]
    
    BL --> EXT[External Services]
    
    subgraph Database
        DB1[(Users)]
        DB2[(Books)]
        DB3[(Payments)]
        DB4[(Borrowings)]
    end
    
    subgraph External
        EMAIL[Email Service]
        STORAGE[File Storage]
        GATEWAY[Payment Gateway]
    end
    
    DA --> Database
    EXT --> External
```

## 6. Security and Access Control

```mermaid
flowchart TB
    REQUEST[User Request] --> AUTH[Authentication Check]
    AUTH -->|Pass| ROLE[Role Verification]
    AUTH -->|Fail| DENY[Access Denied]
    
    ROLE --> PERM{Check Permissions}
    PERM -->|Authorized| ALLOW[Allow Access]
    PERM -->|Unauthorized| DENY
    
    ALLOW --> LOG[Log Activity]
    LOG --> RESPONSE[Return Response]
    
    subgraph Security
        CSRF[CSRF Protection]
        XSS[XSS Prevention]
        SQL[SQL Injection Protection]
        SESSION[Session Management]
    end
    
    AUTH --> Security
```

## 7. Notification System

```mermaid
flowchart TD
    EVENT[System Event] --> TYPE{Event Type}
    
    TYPE -->|Due Date| DUE[Due Date Reminder]
    TYPE -->|Fine| FINE[Fine Notification] 
    TYPE -->|Payment| PAYMENT[Payment Confirmation]
    TYPE -->|System| SYSTEM[System Alert]
    
    DUE --> COLOR{Priority Level}
    FINE --> COLOR
    PAYMENT --> COLOR
    SYSTEM --> COLOR
    
    COLOR -->|Critical| RED[Red Alert]
    COLOR -->|Warning| YELLOW[Yellow Warning]
    COLOR -->|Success| GREEN[Green Success]
    COLOR -->|Info| BLUE[Blue Info]
    
    RED --> SEND[Send to User]
    YELLOW --> SEND
    GREEN --> SEND
    BLUE --> SEND
    
    SEND --> DISPLAY[Display Notification]
```

## 8. E-Book Management

```mermaid
flowchart TD
    UPLOAD[Admin Uploads E-book] --> VALIDATE[Validate PDF]
    VALIDATE -->|Valid| PROCESS[Process File]
    VALIDATE -->|Invalid| ERROR[Show Error]
    
    PROCESS --> STORE[Store in System]
    STORE --> CATEGORIZE[Assign Category]
    CATEGORIZE --> INDEX[Index Content]
    
    INDEX --> AVAILABLE[Make Available]
    AVAILABLE --> ACCESS{User Access}
    
    ACCESS -->|Student| SUB{Has Subscription?}
    ACCESS -->|Lecturer| ALLOW[Allow Reading]
    ACCESS -->|Staff/Admin| ALLOW
    
    SUB -->|Yes| ALLOW
    SUB -->|No| RESTRICT[Restrict Access]
    
    ALLOW --> READER[Online PDF Reader]
    READER --> TRACK[Track Usage]
```
