# apparatusL3

apparatusL3 is an application designed to schedule and manage L3 meetings. The application provides functionalities for admins, moderators, and participants to effectively manage meetings, including adding agendas and action items, meeting attendence and tracking the status of these items.

## Project Structure

- **apparatusl3**: Main project folder
- **l3users**: Handles user-related functionalities including admin, moderators, and participants
- **l3meetings**: Manages meeting schedules, agendas, and action items
- **invites**: Handles meeting invites and notifications
- **sitesettings**: Custom setting manages holidays list, email settings etc.

## Features

- **User Management**: Admin, Moderators, and Participants
- **Meeting Management**: Schedule and manage meetings
- **Agenda Management**: Add and manage meeting agendas
- **Action Items**: Add and manage action items
- **Status Tracking**: Track the status of agendas and action items
- **Attendance Recording**: All user attendance present in the meeting.

## Setup and Installation

### Prerequisites

- Python 3.x
- Django==5 or higher
- Anaconda (for environment management)

### Installation Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abhijeet-infobeans/apparatusl3.git
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    conda create --name appratusl3-internal-app-dev python=3.x
    conda activate appratusl3-internal-app-dev
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Make migrations and apply them**:
    ```bash
    python manage.py makemigrations l3users
    python manage.py makemigrations l3meetings
    python manage.py makemigrations invites
    python manage.py migrate
    ```

5. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

## Usage

### Running the Server

To start the Django development server, run:
```bash
python manage.py runserver
```