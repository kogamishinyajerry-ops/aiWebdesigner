'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui/badge'

interface NavItem {
  title: string
  href: string
  icon?: React.ReactNode
  badge?: string | number
}

interface SidebarSection {
  title: string
  items: NavItem[]
}

const sidebarSections: SidebarSection[] = [
  {
    title: '设计工具',
    items: [
      { title: '图像生成', href: '/generator/image', badge: '新' },
      { title: 'SVG生成', href: '/generator/svg' },
      { title: '图标生成', href: '/generator/icon' },
      { title: '背景纹理', href: '/generator/background' },
    ],
  },
  {
    title: '代码生成',
    items: [
      { title: 'Design to Code', href: '/editor/design-to-code' },
      { title: 'UI组件库', href: '/editor/components' },
      { title: '模板库', href: '/editor/templates' },
    ],
  },
  {
    title: '项目管理',
    items: [
      { title: '我的项目', href: '/dashboard/projects' },
      { title: '收藏夹', href: '/dashboard/favorites' },
      { title: '历史记录', href: '/dashboard/history' },
      { title: '团队协作', href: '/dashboard/team', badge: 'Pro' },
    ],
  },
]

interface SidebarProps {
  className?: string
}

export function Sidebar({ className }: SidebarProps) {
  const pathname = usePathname()

  return (
    <aside
      className={cn(
        'hidden md:flex w-64 flex-col border-r bg-background',
        className
      )}
    >
      <div className="flex flex-1 flex-col overflow-y-auto py-4">
        {sidebarSections.map((section, index) => (
          <div key={section.title} className="px-3 mb-6">
            <h3 className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {section.title}
            </h3>
            <div className="space-y-1">
              {section.items.map((item) => {
                const isActive = pathname === item.href
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      'flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                      isActive
                        ? 'bg-primary/10 text-primary'
                        : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                    )}
                  >
                    <span className="flex items-center gap-3">
                      {item.icon}
                      {item.title}
                    </span>
                    {item.badge && (
                      <Badge variant={item.badge === '新' ? 'default' : 'secondary'} className="text-xs">
                        {item.badge}
                      </Badge>
                    )}
                  </Link>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="border-t p-4">
        <div className="rounded-lg bg-gradient-to-r from-purple-500/10 to-pink-500/10 p-4">
          <p className="text-xs font-semibold text-foreground mb-1">
            升级到 Pro
          </p>
          <p className="text-xs text-muted-foreground mb-3">
            解锁所有高级功能
          </p>
          <button className="w-full rounded-md bg-primary px-3 py-2 text-xs font-medium text-primary-foreground hover:bg-primary/90 transition-colors">
            立即升级
          </button>
        </div>
      </div>
    </aside>
  )
}
