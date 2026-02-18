'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { apiService } from '@/lib/api-service'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

const codePresets = [
  { name: '登录表单', prompt: '现代登录表单,包含邮箱密码输入,记住我,忘记密码按钮' },
  { name: '产品卡片', prompt: '产品展示卡片,包含图片,标题,描述,价格,购买按钮' },
  { name: '导航栏', prompt: '响应式导航栏,包含logo,菜单链接,搜索框,用户头像' },
  { name: '定价表', prompt: '三栏定价表,包含基础版,专业版,企业版,特性列表' },
]

const frameworks = [
  { id: 'tailwind', name: 'Tailwind CSS' },
  { id: 'css', name: 'CSS Modules' },
  { id: 'styled', name: 'Styled Components' },
]

export default function CodeGeneratorPage() {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedCode, setGeneratedCode] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [selectedFramework, setSelectedFramework] = useState('tailwind')

  const handleGenerate = async () => {
    if (!prompt.trim()) return

    setIsGenerating(true)
    setError(null)
    try {
      const response = await apiService.generateCode({
        prompt: prompt.trim(),
        framework: selectedFramework,
        component_type: 'component',
      })

      if (response.success && response.code) {
        setGeneratedCode(response.code)
      } else {
        throw new Error('生成失败')
      }
    } catch (error) {
      console.error('代码生成失败:', error)
      setError(error instanceof Error ? error.message : '生成失败，请重试')
    } finally {
      setIsGenerating(false)
    }
  }

  const handlePresetClick = (presetPrompt: string) => {
    setPrompt(presetPrompt)
  }

  const handleCopy = () => {
    if (!generatedCode) return
    navigator.clipboard.writeText(generatedCode)
  }

  const handleDownload = () => {
    if (!generatedCode) return
    const blob = new Blob([generatedCode], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `generated-code-${Date.now()}.tsx`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="container mx-auto space-y-6 animate-in">
        {/* Back Button */}
        <Link href="/">
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            返回首页
          </Button>
        </Link>

        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            代码生成器
          </h1>
          <p className="text-muted-foreground mt-2">
            使用AI将设计描述转换为可运行的代码
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Input */}
          <div className="lg:col-span-1 space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>设计描述</CardTitle>
                <CardDescription>
                  描述您想要的UI组件或页面
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    提示词
                  </label>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="例如: 现代登录表单,包含邮箱密码输入,记住我,忘记密码按钮..."
                    className="w-full h-32 px-3 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-ring resize-none"
                  />
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">
                    快捷预设
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {codePresets.map((preset) => (
                      <Button
                        key={preset.name}
                        variant="outline"
                        size="sm"
                        className="h-auto py-2 px-3 text-xs justify-start"
                        onClick={() => handlePresetClick(preset.prompt)}
                      >
                        {preset.name}
                      </Button>
                    ))}
                  </div>
                </div>

                <Button
                  onClick={handleGenerate}
                  disabled={!prompt.trim() || isGenerating}
                  variant="gradient"
                  className="w-full"
                >
                  {isGenerating ? '生成中...' : '生成代码'}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>代码设置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    框架
                  </label>
                  <select
                    value={selectedFramework}
                    onChange={(e) => setSelectedFramework(e.target.value)}
                    className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                  >
                    {frameworks.map((fw) => (
                      <option key={fw.id} value={fw.id}>
                        {fw.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="text-xs text-muted-foreground">
                  <p>生成的代码基于 React + TypeScript</p>
                  <p className="mt-2">支持自定义样式和交互逻辑</p>
                </div>

                {error && (
                  <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                    <p className="text-sm text-destructive">{error}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Panel - Preview */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>生成代码</CardTitle>
                    <CardDescription>
                      生成的代码将显示在这里
                    </CardDescription>
                  </div>
                  {generatedCode && (
                    <div className="flex gap-2">
                      <Badge variant="secondary">React</Badge>
                      <Badge variant="outline">TypeScript</Badge>
                      <Badge variant="outline">
                        {frameworks.find((f) => f.id === selectedFramework)?.name}
                      </Badge>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg border">
                  {isGenerating ? (
                    <div className="p-8 space-y-3">
                      <Skeleton className="h-4 w-full" />
                      <Skeleton className="h-4 w-full" />
                      <Skeleton className="h-4 w-3/4" />
                      <div className="pt-4">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-2/3" />
                      </div>
                    </div>
                  ) : generatedCode ? (
                    <div className="relative">
                      <pre className="p-4 text-xs overflow-x-auto max-h-[500px]">
                        <code>{generatedCode}</code>
                      </pre>
                      <div className="absolute top-2 right-2 flex gap-2">
                        <Button onClick={handleCopy} variant="outline" size="sm">
                          复制
                        </Button>
                        <Button onClick={handleDownload} variant="outline" size="sm">
                          下载
                        </Button>
                        <Button
                          onClick={() => setGeneratedCode(null)}
                          variant="outline"
                          size="sm"
                        >
                          清除
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-16 space-y-4">
                      <div className="text-6xl opacity-50">🎨</div>
                      <div>
                        <p className="text-sm text-muted-foreground mb-2">
                          在左侧输入设计描述并点击生成
                        </p>
                        <p className="text-xs text-muted-foreground">
                          支持多种框架和样式方案
                        </p>
                      </div>
                    </div>
                  )}
                </div>

                {generatedCode && (
                  <div className="mt-4">
                    <h4 className="text-sm font-medium mb-2">使用说明</h4>
                    <div className="bg-muted/50 p-4 rounded-md text-xs space-y-2">
                      <p>1. 复制生成的代码到您的项目中</p>
                      <p>2. 根据需要调整样式和逻辑</p>
                      <p>3. 确保已安装相关依赖</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
