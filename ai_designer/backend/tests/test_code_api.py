"""
Test Code Generation Endpoints
"""

import pytest
from fastapi import status
from unittest.mock import AsyncMock, patch


class TestCodeGeneration:
    """Code generation endpoint tests"""

    @pytest.mark.asyncio
    async def test_generate_code_missing_description(self, client):
        """Test code generation without description"""
        response = await client.post(
            "/api/v1/code/generate",
            json={}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_generate_code_with_description(self, client):
        """Test code generation with description"""
        with patch('api.v1.endpoints.code.code_service') as mock_service:
            mock_result = {
                "code": """import React from 'react';

export const TestComponent: React.FC = () => {
  return <div>Hello World</div>;
};""",
                "framework": "react",
                "language": "typescript",
                "component_name": "TestComponent",
                "with_tailwind": True,
                "metadata": {"line_count": 5}
            }
            mock_service.design_to_code = AsyncMock(return_value=mock_result)

            response = await client.post(
                "/api/v1/code/generate",
                json={
                    "description": "A simple React component",
                    "framework": "react",
                    "language": "typescript"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "code" in data
            assert "React" in data["code"]

    @pytest.mark.asyncio
    async def test_get_frameworks(self, client):
        """Test getting supported frameworks"""
        response = await client.get("/api/v1/code/frameworks")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "frameworks" in data
        framework_ids = [f["id"] for f in data["frameworks"]]
        assert "react" in framework_ids
        assert "vue" in framework_ids


class TestComponentLibrary:
    """Component library tests"""

    @pytest.mark.asyncio
    async def test_generate_component_library(self, client):
        """Test component library generation"""
        with patch('api.v1.endpoints.code.code_service') as mock_service:
            mock_components = [
                {
                    "component_name": "Button",
                    "code": "export const Button = () => <button>Click</button>",
                    "framework": "react",
                    "language": "typescript"
                }
            ]
            mock_service.generate_component_library = AsyncMock(return_value=mock_components)

            response = await client.post(
                "/api/v1/code/component-library",
                params={
                    "theme": "modern"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "components" in data


class TestCodeOptimization:
    """Code optimization tests"""

    @pytest.mark.asyncio
    async def test_optimize_code(self, client):
        """Test code optimization"""
        with patch('api.v1.endpoints.code.code_service') as mock_service:
            mock_result = {
                "optimized_code": "/* Optimized */ const x = 1;",
                "suggestions": ["Removed unused variables"],
                "original_size": 100,
                "optimized_size": 80
            }
            mock_service.optimize_code = AsyncMock(return_value=mock_result)

            response = await client.post(
                "/api/v1/code/optimize",
                json={
                    "code": "const x = 1;",
                    "framework": "react"
                }
            )
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "optimized_code" in data
