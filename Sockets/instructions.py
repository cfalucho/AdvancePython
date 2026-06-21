# Assignment: Socket-Based Client/Server System
# This project implements a TCP socket client and TCP socket server that exchange SQL queries. The server executes incoming queries using SQLite. A Tkinter GUI launches both components, displays logs, and provides controls for interaction. The focus is on socket communication, JSON message passing, and integration with QueryBuilder and CommandExecutor. The required GUI and threading structure follow the Socket Dice Example, including the use of background threads to keep the interface responsive.
#
# System Architecture
# Server
#
# Listens on a TCP port
# Accepts a single client connection
# Receives JSON-formatted messages
# Executes SQL queries using CommandExecutor
# Logs all received queries and results
# Client
#
# Connects to the server via TCP
# Loads CSV data into a DataFrame
# Generates SQL queries using QueryBuilder
# Serializes queries as JSON and sends them to the server
# Logs all actions to the GUI
# Tkinter GUI
#
# Launches the client and server
# Displays separate log windows
# Provides a button to send queries
# Uses the same threading and logging pattern demonstrated in the Socket Dice Example

# Client Class Requirements
# Establish a TCP socket connection to the server
# Load CSV data into a DataFrame
# Generate SQL queries using QueryBuilder
# Serialize each query as JSON and transmit it
# Log all actions using the Dice Example logging pattern
# Follow the structural layout of the Dice Example client
# Message Format
#
# Each message sent over the socket must follow this structure:
#
# {
#   "query": "<SQL string>"
# }
# Server Class Requirements
# Listen on a TCP port and accept one client connection
# Receive JSON messages from the client
# Extract SQL queries and execute them using CommandExecutor
# Log all received queries and execution results
# Follow the structural layout of the Dice Example server
# Tkinter GUI Requirements
# The GUI should follow the same design principles as the Socket Dice Example. Its responsibilities include launching the client and server, displaying logs, and providing user controls. The primary focus of the assignment remains the socket logic.
#
# GUI Structure
#
# Create two log windows: Server Log and Client Log
# Use distinct background colors for each log window
# Provide buttons:
# Start Server
# Start Client
# Send Queries
# Launch the client and server in background threads using the Dice Example pattern
# Update the GUI logs using the same log_message() helper approach
# The Socket Dice Example is the reference for GUI structure, threading, and log routing
# Functional Requirements
# Client Behavior
#
# Load CSV files and construct a DataFrame
# Generate SQL queries using QueryBuilder
# Send multiple queries in a batch
# Log each generated and transmitted query
# Server Behavior
#
# Receive serialized JSON messages
# Execute queries in arrival order
# Log all actions
# Communication Rules
#
# All communication must use TCP sockets
# Messages must be serialized (JSON recommended)
# No shared memory or global variables may be used for communication
# The server must handle client disconnects gracefully
# The GUI remains responsive (Dice Example pattern)