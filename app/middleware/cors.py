from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app, frontend_url: str):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
