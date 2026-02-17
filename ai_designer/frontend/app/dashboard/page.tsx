'use client'

import { AppLayout } from '@/components/layout/app-layout'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Button } from '@/components/ui/button'

const stats = [
  { label: '总生成数', value: '1,234', change: '+12%', positive: true },
  { label: '本月使用', value: '456', change: '+8%', positive: true },
  { label: '项目数量', value: '12', change: '+2', positive: true },
  { label: '剩余额度', value: '8,543', change: '无限', positive: true },
]

const recentProjects = [
  { id: 1, name: '电商平台重构', type: '图像生成', date: '2小时前', status: 'completed' },
  { id: 2, name: 'SaaS Dashboard', type: 'SVG生成', date: '5小时前', status: 'in-progress' },
  { id: 3, name: '登录页设计', type: '图像生成', date: '1天前', status: 'completed' },
  { id: 4, name: 'Icon Set', type: '图标生成', date: '2天前', status: 'completed' },
]

export default function DashboardPage() {
  return (
    <AppLayout>
      <div className="space-y-6 animate-in">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              仪表板
            </h1>
            <p className="text-muted-foreground mt-2">
              欢迎回来! 这是您的项目概览
            </p>
          </div>
          <Button variant="gradient">新建项目</Button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, index) => (
            <Card key={index}>
              <CardHeader className="pb-2">
                <CardDescription>{stat.label}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-baseline gap-2">
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <Badge
                    variant={stat.positive ? 'default' : 'secondary'}
                    className="text-xs"
                  >
                    {stat.change}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Projects */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>最近项目</CardTitle>
                <CardDescription>
                  您最近创建和编辑的项目
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentProjects.map((project) => (
                    <div
                      key={project.id}
                      className="flex items-center justify-between p-4 rounded-lg border hover:bg-muted/50 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold">
                          {project.name[0]}
                        </div>
                        <div>
                          <div className="font-medium">{project.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {project.type} · {project.date}
                          </div>
                        </div>
                      </div>
                      <Badge
                        variant={project.status === 'completed' ? 'default' : 'secondary'}
                      >
                        {project.status === 'completed' ? '已完成' : '进行中'}
                      </Badge>
                    </div>
                  ))}
                </div>
                <Button variant="outline" className="w-full mt-4">
                  查看全部项目
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>快速开始</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">🖼️</span> 生成图像
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">📐</span> 生成SVG
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">🎨</span> Design to Code
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>使用提示</CardTitle>
              </CardDescription>
              <CardContent>
                <div className="space-y-3 text-sm text-muted-foreground">
                  <div className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    <span>使用详细的描述词获得更好的效果</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    <span>参考预设模板快速上手</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    <span>保存常用的设计风格</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
