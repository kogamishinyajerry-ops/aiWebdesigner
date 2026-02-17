"use client"

import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "@/components/ui/toast"
import { useToast } from "@/hooks/use-toast"
import { Check, X, Info, AlertTriangle } from "lucide-react"

export function Toaster() {
  const { toasts } = useToast()

  return (
    <ToastProvider>
      {toasts.map(function ({ id, title, description, action, variant, ...props }) {
        const icon = {
          success: <Check className="w-5 h-5" />,
          error: <X className="w-5 h-5" />,
          info: <Info className="w-5 h-5" />,
          warning: <AlertTriangle className="w-5 h-5" />,
        }[variant || "info"]

        return (
          <Toast key={id} variant={variant} {...props}>
            <div className="flex gap-3">
              {icon}
              <div className="flex-1">
                {title && <ToastTitle>{title}</ToastTitle>}
                {description && (
                  <ToastDescription>{description}</ToastDescription>
                )}
              </div>
              {action}
              <ToastClose />
            </div>
          </Toast>
        )
      })}
      <ToastViewport />
    </ToastProvider>
  )
}
