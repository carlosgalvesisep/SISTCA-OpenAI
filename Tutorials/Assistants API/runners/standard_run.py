def std_run (thread_id, assistant_id, client):
    run = client.beta.threads.runs.create_and_poll(
        thread_id = thread_id,
        assistant_id = assistant_id,
        instructions = "Please address the user as SISTCA student."
    )   

    if run.status == 'completed': 

        messages = client.beta.threads.messages.list(
            thread_id = thread_id
        )

        if messages.data[0].content[0].type == 'image_file':
            return(messages.data[0].content[0].image_file.file_id)

        return(messages.data[0].content[0].text.value)        

    else:
        return(run.status)