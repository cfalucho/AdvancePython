# Assignment: Threaded Producer/Consumer
# Overview
# Build a threaded, class-based client/server system using the Producer/Consumer model.
# Client acts as the Producer of SQL queries.
# Server acts as the Consumer that executes them.
# All communication flows through a shared thread-safe queue.
# A Tkinter GUI controls both components and displays logs.
#
# Objective
# The program includes:
#
# A Tkinter GUI running in the main thread
# A Client thread (Producer)
# A Server thread (Consumer)
# A shared queue for all client-to-server messages
# Integration with QueryBuilder and CommandExecutor
# Client (Producer)
#
# Loads CSV data into a DataFrame
# Uses QueryBuilder to generate SQL queries
# Attaches sequence numbers to each query
# Places queries into the shared queue
# Sends activity updates back to the GUI through a thread-safe mechanism
# Server (Consumer)
# The Server runs in its own thread and:
#
# Creates and manages the SQLite database
# Uses CommandExecutor to run incoming queries
# Retrieves queries from the shared queue
# Processes queries sequentially
# Tracks the next expected sequence number
# Rejects out-of-order queries and logs the reason
# Reports activity back to the GUI through a thread-safe mechanism
# Tkinter GUI
# Controls
# Start Server
# Start Client
# Send Queries
# Optional: Stop Server / Stop Client
# Status Indicators
# Server: Running / Stopped
# Client: Running / Stopped
# Logs
# Server Log: received queries, execution order, rejections
# Client Log: generated queries, submissions
# Thread Safety
# Tkinter widgets are updated only from the main thread
# Use a safe mechanism (queue or scheduled callbacks) for log updates
# Long-running work stays in background threads so the GUI remains responsive
# Functional Requirements
# Client produces SQL queries and places them into the shared queue
# Server consumes queries and executes them sequentially
# Client may send multiple queries in a batch
# Each query includes a sequence number
# Server enforces ordering and rejects out-of-order queries
# Both logs show accepted and rejected queries
# GUI should allow demonstrating correct and incorrect ordering
# All communication goes through the shared queue
# No shared mutable state outside the queue
# Internal queues may be used for GUI logging
# Deliverables
# Tkinter GUI
# Threaded Client class
# Threaded Server class
# Queue-based communication
# QueryBuilder and CommandExecutor integration