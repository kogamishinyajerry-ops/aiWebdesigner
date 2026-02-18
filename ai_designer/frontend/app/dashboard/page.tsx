'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import Link from 'next/link'
import { Image, Palette, Code2, Sparkles, TrendingUp, Clock, Zap } from 'lucide-react'

const stats = [
  { label: '总生成数', value: '1,234', change: '+12%', positive: true, icon: TrendingUp },
  { label: '本月使用', value: '456', change: '+8%', positive: true, icon: Clock },
  { label: '项目数量', value: '12', change: '+2', positive: true, icon: Sparkles },
  { label: '剩余额度', value: '∞', change: '无限', positive: true, icon: Zap },
]

const recentProjects = [
  { id: 1, name: '电商平台重构', type: '图像生成', date: '2小时前', status: 'completed', icon: Image },
  { id: 2, name: 'SaaS Dashboard', type: 'SVG生成', date: '5小时前', status: 'in-progress', icon: Palette },
  { id: 3, name: '登录页设计', type: '图像生成', date: '1天前', status: 'completed', icon: Image },
  { id: 4, name: 'UI组件库', type: '代码生成', date: '2天前', status: 'completed', icon: Code2 },
]

const quickActions = [
  {
    title: '生成图像',
    description: '创建高质量网页图像',
    icon: Image,
    href: '/generator/image',
    color: 'from-purple-500 to-pink-500',
  },
  {
    title: '生成SVG',
    description: '创建可缩放矢量图形',
    icon: Palette,
    href: '/generator/svg',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    title: '代码生成',
    description: '设计到代码转换',
    icon: Code2,
    href: '/generator/code',
    color: 'from-green-500 to-emerald-500',
  },
]

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                仪表板
              </h1>
              <p className="text-muted-foreground mt-1">
                欢迎回来！这是您的项目概览
              </p>
            </div>
            <Button variant="gradient">新建项目</Button>
          </div>

          {/* Navigation Tabs */}
          <div className="flex gap-4 mt-6">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                activeTab === 'overview'
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
            >
              概览
            </button>
            <button
              onClick={() => setActiveTab('projects')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                activeTab === 'projects'
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
            >
              项目
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                activeTab === 'analytics'
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted'
              }`}
            >
              分析
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-6 space-y-6">
        {activeTab === 'overview' && (
          <>
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {stats.map((stat, index) => {
                const Icon = stat.icon
                return (
                  <Card key={index}>
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardDescription className="flex items-center gap-2">
                          <Icon className="w-4 h-4" />
                          {stat.label}
                        </CardDescription>
                      </div>
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
                )
              })}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Recent Projects */}
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle>最近项目</CardTitle>
                        <CardDescription>
                          您最近创建和编辑的项目
                        </CardDescription>
                      </div>
                      <Button variant="ghost" size="sm">
                        查看全部
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {recentProjects.map((project) => {
                        const Icon = project.icon
                        return (
                          <div
                            key={project.id}
                            className="flex items-center justify-between p-4 rounded-lg border hover:bg-muted/50 transition-colors"
                          >
                            <div className="flex items-center gap-4">
                              <div className={`h-10 w-10 rounded-lg bg-gradient-to-br ${project.icon === Image ? 'from-purple-500 to-pink-500' : project.icon === Palette ? 'from-blue-500 to-cyan-500' : 'from-green-500 to-emerald-500'} flex items-center justify-center text-white`}>
                                <Icon className="w-5 h-5" />
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
                        )
                      })}
                    </div>
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
                    {quickActions.map((action) => (
                      <Link key={action.href} href={action.href}>
                        <Button
                          variant="outline"
                          className="w-full justify-start h-auto py-3"
                        >
                          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${action.color} flex items-center justify-center text-white mr-3`}>
                            <action.icon className="w-5 h-5" />
                          </div>
                          <div className="text-left">
                            <div className="font-medium">{action.title}</div>
                            <div className="text-xs text-muted-foreground">
                              {action.description}
                            </div>
                          </div>
                        </Button>
                      </Link>
                    ))}
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>使用提示</CardTitle>
                  <CardDescription>
                    提高设计效果的技巧
                  </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3 text-sm text-muted-foreground">
                      <div className="flex items-start gap-2">
                        <Sparkles className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                        <span>使用详细的描述词获得更好的效果</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <Sparkles className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                        <span>参考预设模板快速上手</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <Sparkles className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                        <span>保存常用的设计风格和配色</span>
                      </div>
                      <div className="flex items-start gap-2">
                        <Sparkles className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                        <span>批量生成可提高效率</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </>
        )}

        {activeTab === 'projects' && (
          <Card>
            <CardHeader>
              <CardTitle>所有项目</CardTitle>
              <CardDescription>管理您的所有设计项目</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <Sparkles className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">项目列表正在开发中...</p>
              </div>
            </CardContent>
          </Card>
        )}

        {activeTab === 'analytics' && (
          <Card>
            <CardHeader>
              <CardTitle>使用分析</CardTitle>
              <CardDescription>查看您的使用统计和趋势</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <TrendingUp className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">分析功能正在开发中...</p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
