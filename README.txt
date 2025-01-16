
# Python
Python version: 3.11 used to get SQLalchemy working
Venv:  ~/Documents/dev/Environments/sanic311
source  ~/Documents/dev/Environments/sanic311/bin/activate 
# Run the server
python server.py


# Next
# Build the Next.js app
cd frontend/next
npm run build
# Start the production server
npm start

# Adding new ShadCN components
npx shadcn@latest init
npx shadcn@latest add button