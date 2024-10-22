  # Assuming TrafficCount is defined in this file
def backup_db():
    import csv
    import os
    from sqlalchemy import desc, create_engine
    from sqlalchemy.orm import sessionmaker
    from create_db import TrafficCount

    engine = create_engine('sqlite:///C:/Users/johnb/PycharmProjects/FA24_Capstone_SoMuchForSubtlety/backend/database/my_database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Path for the CSV file to store older records
    csv_file_path = "C:\\Users\\johnb\\PycharmProjects\\FA24_Capstone_SoMuchForSubtlety\\backend\\database\\DB_BACKUP.csv"

    # Step 1: Query the TrafficCount table and sort by update_time in descending order (newest first)
    total_entries = session.query(TrafficCount).count()

    if total_entries > 800:
        # Step 2: Get all but the 400 most recent entries
        entries_to_export = session.query(TrafficCount).order_by(desc(TrafficCount.traffic_time))[200:]

        # Step 3: Write the results to a CSV file
        with open(csv_file_path, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if os.path.getsize(csv_file_path) == 0:
                writer.writerow(
                    ['id', 'cam_id', 'traffic_count', 'traffic_time','max_traffic_count','max_traffic_time'])
            # Write the entries to the CSV
            for entry in entries_to_export:
                writer.writerow([entry.id, entry.cam_id, entry.traffic_count, entry.traffic_time, entry.max_traffic_count, entry.max_traffic_time])

        # Step 4: Delete the written entries from the database
        for entry in entries_to_export:
            session.delete(entry)

        # Commit the changes to persist the deletion
        session.commit()
    else:
        print("No records to archive. Less than or equal to 400 entries in the database.")

    session.close()