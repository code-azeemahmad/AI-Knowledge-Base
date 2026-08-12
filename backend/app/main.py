# backend\app\main.py
import app.core.logging
from app.core.config import settings
from app.core.lifespan import lifespan
from app.routers.document import router as document_router
from app.routers.health import router as health_router
from app.routers.product import router as product_router
from app.routers.rag import router as rag_router
from app.routers.retrieval import router as retrieval_router
from app.routers.search import router as search_router
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from fastapi.openapi.docs import get_swagger_ui_html
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Your existing custom CSS
CUSTOM_SWAGGER_CSS = """
body { background-color: #1e1e1e !important; }
.swagger-ui .info .title, .swagger-ui .info p, .swagger-ui .scheme-container, 
.swagger-ui section.models h4, .swagger-ui .opblock-tag, 
.swagger-ui .opblock .opblock-summary-description, .swagger-ui .opblock .opblock-summary-path { color: #ffffff !important; }
.swagger-ui .scheme-container { background-color: #2a2a2a !important; }
.swagger-ui .opblock-body { background-color: #ffffff !important; color: #000000 !important; }
.swagger-ui .opblock-body table, .swagger-ui .opblock-body label, .swagger-ui .opblock-body p, 
.swagger-ui .opblock-body span, .swagger-ui .opblock-body .parameter__name, .swagger-ui .opblock-body .parameter__type { color: #000000 !important; }
.swagger-ui .highlight-code, .swagger-ui .microlight, .swagger-ui .opblock-body pre, .swagger-ui .opblock-body code { background-color: #2b2b2b !important; color: #ffffff !important; }
.swagger-ui .highlight-code span, .swagger-ui .microlight span { color: #ffffff !important; }
"""

# Custom JavaScript for Keyboard Shortcuts (T, E, R)
KEYBOARD_SHORTCUTS_JS = """
<script>
document.addEventListener('keydown', function(e) {
    // Ignore key presses inside text inputs, textareas, or select dropdowns
    const activeElem = document.activeElement;
    if (activeElem && (activeElem.tagName === 'INPUT' || activeElem.tagName === 'TEXTAREA' || activeElem.tagName === 'SELECT')) {
        return;
    }

    const key = e.key.toUpperCase();

    // 'T' -> Click "Try it out" / "Cancel"
    if (key === 'T') {
        const tryBtn = document.querySelector('.opblock.is-open .btn.try-out__btn');
        if (tryBtn) tryBtn.click();
    }

    // 'E' -> Click "Execute"
    if (key === 'E') {
        const execBtn = document.querySelector('.opblock.is-open .btn.execute');
        if (execBtn) execBtn.click();
    }

    // 'R' -> Click "Clear" / "Reset"
    if (key === 'R') {
        const clearBtn = document.querySelector('.opblock.is-open .btn.btn-clear');
        if (clearBtn) clearBtn.click();
    }
});
</script>
"""


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Docs",
    )

    # Decode HTML body string
    response_body = html_response.body.decode("utf-8")

    # Inject CSS before </head>
    response_body = response_body.replace(
        "</head>", f"<style>{CUSTOM_SWAGGER_CSS}</style></head>"
    )

    # Inject JS shortcuts before </body>
    response_body = response_body.replace(
        "</body>", f"{KEYBOARD_SHORTCUTS_JS}</body>"
    )

    return HTMLResponse(content=response_body)

app.include_router(search_router)
app.include_router(rag_router)
app.include_router(document_router)
app.include_router(product_router)
app.include_router(health_router)   
app.include_router(retrieval_router)   


@app.get("/", tags=["Root"])
async def root():
    return {
        "title": app.title,
        "version": app.version,
        "status": "running",
    }