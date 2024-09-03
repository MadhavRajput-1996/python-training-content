TEMPLATES = [
    {
        'name': 'Action Item Added',
        'subject': 'New Action Item: {action_item_title}',
        'body': """
            <p>Dear {recipient_name},</p>
            <p>A new action item titled <strong><a href="{action_item_link}">{action_item_title}</a></strong> has been assigned to you in Agenda <strong>{action_item_agenda}</strong>.</p>
            <p><strong>Start Date:</strong> {start_date}</p>
            <p><strong>Target End Date:</strong> {target_end_date}</p>
            <p>Please take the necessary actions to address this item.</p>
            <p>Best regards,<br>ApparatusL3 Team</p>
        """,
    },
    {
        'name': 'Action Item Updated',
        'subject': 'Action Item Updated: {action_item_title}',
        'body': """
            <p>Dear {recipient_name},</p>
            <p>The Assigned action item <strong><a href="{action_item_link}">{action_item_title}</a></strong> has been updated.</p>
            <p><strong>Updated By:</strong> {updated_by_name}</p>
            <p><strong>New Details:</strong></p>
            <ul>
                <li><strong>Status:</strong> {status}</li>
                <li><strong>Start Date:</strong> {start_date}</li>
                <li><strong>Target End Date:</strong> {target_end_date}</li>
            </ul>
            <p>Please review the changes and take any necessary actions.</p>
            <p>Best regards,<br>ApparatusL3 Team</p>
        """,
    },
    {
        'name': 'Action Item Closed',
        'subject': 'Action Item Closed: {action_item_title}',
        'body': """
            <p>Dear {recipient_name},</p>
            <p>The action item titled <strong><a href="{action_item_link}">{action_item_title}</a></strong> status has been marked as closed by the Team.</p>
            <p>Thank you for your efforts in completing this action item.</p>
            <p>Best regards,<br>ApparatusL3 Team</p>
        """,
    },
    {
        'name': 'Action Item Response',
        'subject': 'Response to Action Item: {action_item_title}',
        'body': """
            <p>Dear {recipient_name},</p>
            <p>A response has been added to the action item titled <strong><a href="{action_item_link}">{action_item_title}</a></strong>.</p>
            <p>Please review the response and take any further necessary actions.</p>
            <p>Best regards,<br>ApparatusL3 Team</p>
        """,
    },
    {
        'name': 'Meeting Invitation',
        'subject': 'You’re Invited: {meeting_title}',
        'body': """
            <p>Dear {recipient_name},</p>
            <p>You are invited to attend the meeting <strong>{meeting_title}</strong>.</p>
            <p><strong>Description:</strong> {meeting_description}</p>
            <p><strong>Date:</strong> {meeting_date}</p>
            <p><strong>Time:</strong> {meeting_time}</p>
            <p><strong>Agenda:</strong></p>
            <ul>
                {meeting_agenda_items}
            </ul>
            <p>Looking forward to your participation.</p>
            <p>Best regards,<br>{sender_name}</p>
        """,
    },
    {
        'name': 'Meeting Update',
        'subject': 'Meeting {meeting_title} Updated ',
        'body': """
            <p>Dear {recipient_name},</p>
            <p>You are invited to attend the meeting <strong>{meeting_title}</strong>.</p>
            <p><strong>Description:</strong> {meeting_description}</p>
            <p><strong>Date:</strong> {meeting_date}</p>
            <p><strong>Time:</strong> {meeting_time}</p>
            <p><strong>Agenda:</strong></p>
            <ul>
                {meeting_agenda_items}
            </ul>
            <p>Looking forward to your participation.</p>
            <p>Best regards,<br>{sender_name}</p>
        """,
    },
]
