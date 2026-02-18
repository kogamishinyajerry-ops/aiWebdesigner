"""
Code Generation Endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid
from loguru import logger

from services import code_service

router = APIRouter()


class CodeGenerationRequest(BaseModel):
    """Code generation request"""
    description: str = Field(..., description="Description of the design")
    framework: str = Field(default="react", description="Target framework (react, vue, svelte)")
    language: str = Field(default="typescript", description="Programming language")
    with_tailwind: bool = Field(default=True, description="Use Tailwind CSS")
    component_name: str = Field(default="GeneratedComponent", description="Component name")


class CodeGenerationResponse(BaseModel):
    """Code generation response"""
    success: bool
    code: str
    framework: str
    language: str
    component_name: str
    with_tailwind: bool
    metadata: Optional[dict] = None
    request_id: Optional[str] = None


@router.post("/generate", response_model=CodeGenerationResponse)
async def generate_code(request: CodeGenerationRequest, http_request: Request):
    """
    Generate code from design description
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating {request.framework} code: {request.description}")

        # Generate code
        result = await code_service.design_to_code(
            description=request.description,
            framework=request.framework,
            language=request.language,
            with_tailwind=request.with_tailwind,
            component_name=request.component_name
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        logger.info(f"[{request_id}] Code generated in {generation_time:.2f}s")

        return CodeGenerationResponse(
            success=True,
            code=result["code"],
            framework=result["framework"],
            language=result["language"],
            component_name=result["component_name"],
            with_tailwind=result["with_tailwind"],
            metadata=result["metadata"],
            request_id=request_id
        )

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Code generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class DesignToCodeResponse(BaseModel):
    """Design to code response"""
    success: bool
    message: str
    framework: str


@router.post("/design-to-code", response_model=DesignToCodeResponse)
async def design_to_code(
    image: UploadFile = File(...),
    framework: str = "react",
    language: str = "typescript",
    with_tailwind: bool = True
):
    """
    Convert design image to code
    """
    try:
        # TODO: Implement image-to-code conversion using CLIP
        return {
            "success": False,
            "message": "Image-to-code conversion coming soon",
            "framework": framework
        }
    except Exception as e:
        logger.error(f"Design-to-code conversion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class ComponentLibraryRequest(BaseModel):
    """Component library request"""
    theme: str = Field(default="modern", description="Component library theme")
    components: Optional[List[str]] = Field(None, description="List of components to generate")


@router.post("/component-library")
async def generate_component_library(
    request: ComponentLibraryRequest,
    http_request: Request = None
):
    """
    Generate a component library
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating component library with theme: {request.theme}")

        # Generate component library
        components = await code_service.generate_component_library(
            theme=request.theme,
            components=request.components
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        # Prepare response
        component_list = []
        for comp in components:
            component_list.append({
                "name": comp["component_name"],
                "code": comp["code"],
                "framework": comp["framework"],
                "language": comp["language"]
            })

        logger.info(f"[{request_id}] Generated {len(components)} components in {generation_time:.2f}s")

        return {
            "success": True,
            "theme": request.theme,
            "components": component_list,
            "generation_time": generation_time,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Component library generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class OptimizeCodeRequest(BaseModel):
    """Code optimization request"""
    code: str = Field(..., description="Code to optimize")
    framework: str = Field(default="react", description="Target framework")


@router.post("/optimize")
async def optimize_code(
    request: OptimizeCodeRequest
):
    """
    Optimize existing code
    """
    try:
        request_id = "unknown"

        logger.info(f"[{request_id}] Optimizing code")

        # Optimize code
        result = await code_service.optimize_code(request.code, request.framework)

        logger.info(f"[{request_id}] Code optimized")

        return {
            "success": True,
            "optimized_code": result["optimized_code"],
            "suggestions": result["suggestions"],
            "original_size": result["original_size"],
            "optimized_size": result["optimized_size"],
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Code optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frameworks")
async def get_supported_frameworks():
    """
    Get supported frameworks and languages
    """
    return {
        "frameworks": [
            {"id": "react", "name": "React", "languages": ["typescript", "javascript"]},
            {"id": "vue", "name": "Vue.js", "languages": ["typescript", "javascript"]},
            {"id": "svelte", "name": "Svelte", "languages": ["typescript", "javascript"]},
            {"id": "html", "name": "HTML/CSS", "languages": ["javascript"]}
        ],
        "default_framework": "react",
        "default_language": "typescript"
    }
