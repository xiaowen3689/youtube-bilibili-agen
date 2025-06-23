import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Download, Upload, FileText, Languages, CheckCircle, AlertCircle, Play } from 'lucide-react'
import './App.css'

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [videoTitle, setVideoTitle] = useState('')
  const [videoDescription, setVideoDescription] = useState('')
  const [videoTags, setVideoTags] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const steps = [
    { icon: Download, label: '下载YouTube视频', description: '从YouTube下载指定视频' },
    { icon: FileText, label: '提取音频', description: '从视频中提取音频文件' },
    { icon: Languages, label: '生成字幕', description: '使用AI生成原始字幕' },
    { icon: Languages, label: '翻译字幕', description: '将字幕翻译为中文' },
    { icon: FileText, label: '合并双语字幕', description: '创建双语字幕文件' },
    { icon: Upload, label: '上传到B站', description: '将视频上传到哔哩哔哩' }
  ]

  // Poll for status updates when processing
  useEffect(() => {
    let interval
    if (isProcessing) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`${API_BASE_URL}/api/status`)
          const status = await response.json()
          
          setCurrentStep(status.current_step)
          setProgress(status.progress)
          
          if (!status.is_processing) {
            setIsProcessing(false)
            if (status.result) {
              setResult(status.result)
            }
            if (status.error) {
              setError(status.error)
            }
          }
        } catch (err) {
          console.error('Failed to fetch status:', err)
        }
      }, 1000)
    }
    
    return () => {
      if (interval) clearInterval(interval)
    }
  }, [isProcessing])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!youtubeUrl.trim()) {
      setError('请输入YouTube视频链接')
      return
    }

    setIsProcessing(true)
    setCurrentStep(0)
    setProgress(0)
    setError('')
    setResult(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          youtube_url: youtubeUrl,
          video_title: videoTitle,
          video_description: videoDescription,
          video_tags: videoTags
        })
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || '处理请求失败')
      }
      
      // Processing started successfully, status will be updated via polling
    } catch (err) {
      setError('启动处理失败: ' + err.message)
      setIsProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            YouTube 到 B站 智能体
          </h1>
          <p className="text-lg text-gray-600">
            自动下载YouTube视频，生成双语字幕，并上传到哔哩哔哩
          </p>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Play className="h-5 w-5" />
              视频处理配置
            </CardTitle>
            <CardDescription>
              请填写YouTube视频链接和B站上传信息
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  YouTube 视频链接 *
                </label>
                <Input
                  type="url"
                  placeholder="https://www.youtube.com/watch?v=..."
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  disabled={isProcessing}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  B站视频标题
                </label>
                <Input
                  placeholder="请输入视频标题"
                  value={videoTitle}
                  onChange={(e) => setVideoTitle(e.target.value)}
                  disabled={isProcessing}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  视频描述
                </label>
                <Textarea
                  placeholder="请输入视频描述"
                  value={videoDescription}
                  onChange={(e) => setVideoDescription(e.target.value)}
                  disabled={isProcessing}
                  rows={3}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  视频标签
                </label>
                <Input
                  placeholder="请输入标签，用逗号分隔"
                  value={videoTags}
                  onChange={(e) => setVideoTags(e.target.value)}
                  disabled={isProcessing}
                />
              </div>

              <Button 
                type="submit" 
                className="w-full" 
                disabled={isProcessing}
              >
                {isProcessing ? '处理中...' : '开始处理'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {isProcessing && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>处理进度</CardTitle>
              <CardDescription>
                正在执行第 {currentStep + 1} 步，共 {steps.length} 步
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Progress value={progress} className="w-full" />
                
                <div className="grid gap-3">
                  {steps.map((step, index) => {
                    const StepIcon = step.icon
                    const isCompleted = index < currentStep
                    const isCurrent = index === currentStep
                    
                    return (
                      <div 
                        key={index}
                        className={`flex items-center gap-3 p-3 rounded-lg border ${
                          isCompleted 
                            ? 'bg-green-50 border-green-200' 
                            : isCurrent 
                            ? 'bg-blue-50 border-blue-200' 
                            : 'bg-gray-50 border-gray-200'
                        }`}
                      >
                        <div className={`p-2 rounded-full ${
                          isCompleted 
                            ? 'bg-green-100 text-green-600' 
                            : isCurrent 
                            ? 'bg-blue-100 text-blue-600' 
                            : 'bg-gray-100 text-gray-400'
                        }`}>
                          {isCompleted ? (
                            <CheckCircle className="h-4 w-4" />
                          ) : (
                            <StepIcon className="h-4 w-4" />
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium">{step.label}</div>
                          <div className="text-sm text-gray-600">{step.description}</div>
                        </div>
                        {isCompleted && (
                          <Badge variant="secondary" className="bg-green-100 text-green-700">
                            完成
                          </Badge>
                        )}
                        {isCurrent && (
                          <Badge variant="secondary" className="bg-blue-100 text-blue-700">
                            进行中
                          </Badge>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {error && (
          <Alert className="mb-8 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-700">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {result && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-700">
                <CheckCircle className="h-5 w-5" />
                处理完成
              </CardTitle>
              <CardDescription>
                视频已成功处理{result.upload_success ? '并上传到B站' : '，但上传失败'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {result.video_path && (
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">视频文件:</span>
                    <span className="text-sm text-gray-600">{result.video_path}</span>
                  </div>
                )}
                {result.bilingual_srt && (
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">双语字幕:</span>
                    <span className="text-sm text-gray-600">{result.bilingual_srt}</span>
                  </div>
                )}
                <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                  <span className="font-medium">B站上传:</span>
                  <Badge variant="secondary" className={
                    result.upload_success 
                      ? "bg-green-100 text-green-700" 
                      : "bg-red-100 text-red-700"
                  }>
                    {result.upload_success ? '成功' : '失败'}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle>使用说明</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm text-gray-600">
              <p>1. 输入有效的YouTube视频链接</p>
              <p>2. 填写B站上传所需的标题、描述和标签</p>
              <p>3. 点击"开始处理"按钮，系统将自动完成以下步骤：</p>
              <ul className="list-disc list-inside ml-4 space-y-1">
                <li>下载YouTube视频</li>
                <li>提取音频文件</li>
                <li>使用AI生成英文字幕</li>
                <li>将字幕翻译为中文</li>
                <li>合并生成双语字幕</li>
                <li>上传视频到B站</li>
              </ul>
              <p>4. 处理完成后，您可以在B站查看上传的视频</p>
              <p className="text-amber-600 font-medium">注意：请确保后端API服务正在运行 (http://localhost:5000)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App

