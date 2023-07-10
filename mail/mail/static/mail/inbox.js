document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  //NEW
  document.querySelector("#compose-form").addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail_detail').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_mail(id, mailbox){
  console.log(id)
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
        // display the mail
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#mail_detail').style.display = 'block';

        document.querySelector('#mail_detail').innerHTML = `
        <h6>From: ${email.sender}</h6>
        <h6>To: ${email.recipients}</h6>
        <h6>Subject: ${email.subject}</h6>
        <h6>Timestamp: ${email.timestamp}</h6>
        <h8>${email.body}</h8><br>
        <div></div><br>
        <div></div><br>
        `
    
    if(!email.read){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }
    // if sent, then no need for archive button
    // add an archive button
    if(mailbox != 'sent') {
        const element_button = document.createElement('button');
        element_button.innerHTML = email.archived ? "Unarchive" : "Archive";
        element_button.className = email.archived ? "btn btn-success" : "btn btn-warning"; 
        element_button.addEventListener('click', function() {
          fetch(`emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
            archived: !email.archived
          })
      })
        .then(() => {load_mailbox('inbox')})
      });
        document.querySelector('#mail_detail').append(element_button);
      };
    

    // add a reply button
    const element_reply = document.createElement('button');
    element_reply.innerHTML = "Reply"
    element_reply.className = "btn btn-info"
    element_reply.addEventListener('click', function() {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      if(email.subject.split(' ', 1)[0] != "Re:"){
        document.querySelector('#compose-subject').value = "Re: " + email.subject;}
      document.querySelector('#compose-body').value = "'On " + email.timestamp + " " + email.sender + " wrote:' " + email.body;
    });
    document.querySelector('#mail_detail').append(element_reply);
});
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail_detail').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
  
      // ... do something else with emails ...
      emails.forEach(singleEmail => {
        const element = document.createElement('div');
        element.className = "list-group-item active";
        element.innerHTML = `
        <h7>Sender: ${singleEmail.sender}</h4>
        <h5>Subject: ${singleEmail.subject}</h3>
        <p>${singleEmail.timestamp}</p>
        `;

        element.className = singleEmail.read ? 'list-group-item list-group-item-action list-group-item-secondary' : 'list-group-item list-group-item-action'

              element.addEventListener('click', function() {
                view_mail(singleEmail.id, mailbox)
              });
        document.querySelector('#emails-view').append(element);
      })
  });
  
}


function send_email(event) {
event.preventDefault()
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
  };


