# CertiFlow - Bulk Certificate Generator

A web-based project for simplifying bulk certificate generation for participants of events, workshops, and courses.

## Overview

CertiFlow is developed as part of a technical assessment to demonstrate a system for generating personalized certificates for multiple recipients using a predefined template.

The project focuses on bulk processing, recipient data validation, certificate generation, job status tracking, failure handling, and certificate retrieval.

## Objectives

- Generate personalized certificates for multiple recipients in a single request.
- Validate recipient information before processing.
- Generate certificates using a predefined template.
- Track generation progress and individual results.
- Handle individual certificate-generation failures without interrupting other valid recipients.
- Provide access to successfully generated certificates.

## Key Features

- **Bulk Certificate Generation:** Process multiple recipients in one request.
- **Personalized Certificates:** Include recipient-specific information in generated certificates.
- **Input Validation:** Identify missing or invalid recipient data.
- **Job Status Tracking:** Monitor generation progress and processing results.
- **Failure Handling:** Record failed generations while preserving successful results.
- **Certificate Retrieval:** Access generated certificate files.
- **User-Friendly Interface:** Provide a simple and intuitive application experience.

## Technology Stack

- **Frontend:** Next.js, React, TypeScript
- **Development Tools:** v0, npm, Git, GitHub
- **Deployment:** Vercel

Backend technologies, database, PDF-generation library, and testing tools should be added here according to the actual implementation.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Node.js
- npm
- Git

### Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd Bulk_Certificate_Gen
```

Install the dependencies:

```bash
npm install
```

### Run the Development Server

Start the application:

```bash
npm run dev
```

Open [http://localhost:3000](https://certify-git-main-tippalalavanyas-projects.vercel.app) in your browser to view the application.

The application will automatically update when you modify supported source files.

## Project Structure

The project uses the Next.js App Router.

```text
Bulk_Certificate_Gen/
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   └── globals.css
├── public/
├── package.json
├── tsconfig.json
└── README.md
```

Note: Update this structure to match the actual repository.

## Live Demo

The application is deployed on Vercel.

[View Live Application](https://certify-git-main-tippalalavanyas-projects.vercel.app/)

## Assessment Requirements

The project is intended to address the following requirements:

- Bulk certificate generation
- Recipient data validation
- Predefined certificate template
- Job status and progress tracking
- Individual failure handling
- Generated certificate retrieval
- Automated testing and documentation

The completed implementation should be verified against each requirement before submission.

## Future Improvements

- Integrate a Python backend using FastAPI.
- Add relational database support for persistent job tracking.
- Implement background processing for large recipient batches.
- Generate downloadable PDF certificates.
- Expand automated test coverage.
- Improve logging and error reporting.

## Author

Tippala Lavanya

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Learn Next.js](https://nextjs.org/learn)
- [v0 Documentation](https://v0.app/docs)
- [Vercel Documentation](https://vercel.com/docs)
