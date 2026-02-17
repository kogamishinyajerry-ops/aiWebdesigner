'use client'

import { AppLayout } from '@/components/layout/app-layout'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

export default function SettingsPage() {
  return (
    <AppLayout>
      <div className="space-y-6 animate-in">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            设置
          </h1>
          <p className="text-muted-foreground mt-2">
            管理您的账户和偏好设置
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Settings */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>个人资料</CardTitle>
                <CardDescription>
                  更新您的个人信息
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">
                      显示名称
                    </label>
                    <input
                      type="text"
                      defaultValue="设计师"
                      className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">
                      邮箱地址
                    </label>
                    <input
                      type="email"
                      defaultValue="designer@example.com"
                      className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    个人简介
                  </label>
                  <textarea
                    defaultValue="热爱AI设计的前端开发者"
                    rows={3}
                    className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background resize-none"
                  />
                </div>
                <Button variant="gradient">保存更改</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>API 配置</CardTitle>
                <CardDescription>
                  配置外部 API 密钥
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Gemini API Key
                  </label>
                  <input
                    type="password"
                    placeholder="sk-..."
                    className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    FLUX API Key
                  </label>
                  <input
                    type="password"
                    placeholder="sk-..."
                    className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                  />
                </div>
                <Button variant="outline">测试连接</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>偏好设置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">默认图像尺寸</div>
                    <div className="text-sm text-muted-foreground">
                      图像生成的默认尺寸
                    </div>
                  </div>
                  <select className="px-3 py-2 text-sm rounded-md border border-input bg-background">
                    <option>1920 x 1080</option>
                    <option>1280 x 720</option>
                    <option>1080 x 1080</option>
                  </select>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">自动保存</div>
                    <div className="text-sm text-muted-foreground">
                      自动保存项目草稿
                    </div>
                  </div>
                  <Badge variant="default">已启用</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">通知邮件</div>
                    <div className="text-sm text-muted-foreground">
                      接收生成完成通知
                    </div>
                  </div>
                  <Badge variant="outline">已禁用</Badge>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>当前计划</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center space-y-4">
                  <div className="text-4xl">🎯</div>
                  <div>
                    <div className="font-bold text-lg">免费版</div>
                    <div className="text-sm text-muted-foreground">
                      每月 100 次生成
                    </div>
                  </div>
                  <Button variant="gradient" className="w-full">
                    升级到 Pro
                  </Button>
                  <div className="text-xs text-muted-foreground">
                    解锁无限生成和高级功能
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>使用情况</CardTitle>
              </CardDescription>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>本月配额</span>
                      <span>45/100</span>
                    </div>
                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 w-[45%]" />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>存储空间</span>
                      <span>1.2/5 GB</span>
                    </div>
                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 w-[24%]" />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>帮助</CardTitle>
              </CardDescription>
              <CardContent className="space-y-2">
                <Button variant="ghost" className="w-full justify-start">
                  📚 文档
                </Button>
                <Button variant="ghost" className="w-full justify-start">
                  💬 社区
                </Button>
                <Button variant="ghost" className="w-full justify-start">
                  🐛 反馈问题
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
