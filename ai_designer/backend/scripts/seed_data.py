"""
Seed data script
Create initial templates and tags
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models import User, Template, Tag
import uuid


async def create_templates(db: AsyncSession):
    """Create initial templates"""
    templates = [
        # Image templates
        {
            "id": uuid.uuid4(),
            "name": "Hero Banner - Modern",
            "slug": "hero-banner-modern",
            "type": "image",
            "category": "hero",
            "description": "Modern hero banner with clean design",
            "prompt_template": "Modern hero banner for website, {title}, clean design, gradient background, minimal",
            "parameters": '{"width": 1920, "height": 1080, "style": "modern"}',
            "is_public": True,
            "is_official": True,
            "usage_count": 0,
            "rating": 5,
            "order": 1
        },
        {
            "id": uuid.uuid4(),
            "name": "Hero Banner - Glassmorphism",
            "slug": "hero-banner-glassmorphism",
            "type": "image",
            "category": "hero",
            "description": "Hero banner with glassmorphism effect",
            "prompt_template": "Hero banner, {title}, glassmorphism effect, blur, translucent, gradient background",
            "parameters": '{"width": 1920, "height": 1080, "style": "glassmorphism"}',
            "is_public": True,
            "is_official": True,
            "usage_count": 0,
            "rating": 5,
            "order": 2
        },
        {
            "id": uuid.uuid4(),
            "name": "Product Showcase",
            "slug": "product-showcase",
            "type": "image",
            "category": "product",
            "description": "Product showcase image",
            "prompt_template": "Product showcase, {product}, high quality, professional lighting, clean background",
            "parameters": '{"width": 1920, "height": 1080, "style": "minimal"}',
            "is_public": True,
            "is_official": True,
            "usage_count": 0,
            "rating": 5,
            "order": 3
        },
        # SVG templates
        {
            "id": uuid.uuid4(),
            "name": "Minimalist Icon",
            "slug": "icon-minimalist",
            "type": "svg",
            "category": "icon",
            "description": "Minimalist style icon",
            "prompt_template": "Minimalist icon, {icon}, simple lines, clean design",
            "parameters": '{"width": 512, "height": 512, "style": "minimalist"}',
            "is_public": True,
            "is_official": True,
            "usage_count": 0,
            "rating": 5,
            "order": 4
        },
        {
            "id": uuid.uuid4(),
            "name": "Filled Icon",
            "slug": "icon-filled",
            "type": "svg",
            "category": "icon",
            "description": "Filled style icon",
            "prompt_template": "Filled icon, {icon}, solid shapes, vibrant colors",
            "parameters": '{"width": 512, "height": 512, "style": "filled"}',
            "is_public": True,
            "is_official": True,
            "usage_count": 0,
            "rating": 5,
            "order": 5
        },
    ]

    for template_data in templates:
        # Check if template already exists
        from sqlalchemy import select
        result = await db.execute(
            select(Template).where(Template.slug == template_data["slug"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            db_obj = Template(**template_data)
            db.add(db_obj)

    await db.commit()
    print(f"✅ Created {len(templates)} templates")


async def create_tags(db: AsyncSession):
    """Create initial tags"""
    tags = [
        {"name": "Modern", "slug": "modern", "color": "#6366f1", "usage_count": 0},
        {"name": "Minimal", "slug": "minimal", "color": "#1f2937", "usage_count": 0},
        {"name": "Gradient", "slug": "gradient", "color": "#8b5cf6", "usage_count": 0},
        {"name": "Dark", "slug": "dark", "color": "#111827", "usage_count": 0},
        {"name": "Light", "slug": "light", "color": "#f3f4f6", "usage_count": 0},
        {"name": "Glassmorphism", "slug": "glassmorphism", "color": "#a78bfa", "usage_count": 0},
        {"name": "Neumorphism", "slug": "neumorphism", "color": "#d1d5db", "usage_count": 0},
        {"name": "Brutalism", "slug": "brutalism", "color": "#ef4444", "usage_count": 0},
    ]

    for tag_data in tags:
        # Check if tag already exists
        from sqlalchemy import select
        result = await db.execute(
            select(Tag).where(Tag.slug == tag_data["slug"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            db_obj = Tag(**tag_data)
            db.add(db_obj)

    await db.commit()
    print(f"✅ Created {len(tags)} tags")


async def main():
    """Main function"""
    # Create engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        print("🌱 Seeding database...")

        await create_templates(db)
        await create_tags(db)

        print("✅ Database seeded successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
