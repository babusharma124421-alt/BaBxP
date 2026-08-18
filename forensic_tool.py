#!/usr/bin/env python3
"""
Advanced Forensic Recovery Tool - Professional TUI
Complete implementation with color palette, formatting, and all screen layouts
"""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich.tree import Tree
from rich.layout import Layout
from rich.live import Live
from rich import box
import time
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

# ═══════════════════════════════════════════════════════════════════════════
# COLOR PALETTE & THEME CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

custom_theme = Theme({
    # Semantic status colors
    "success": "bold #2ECC40",
    "danger": "bold #FF4136",
    "warning": "bold #FF851B",
    "info": "bold #0074D9",
    "processing": "bold #B10DC9",
    "deleted": "bold #FFDC00",
    "highlight": "bold #7FDBCA",
    "disabled": "dim #AAAAAA",
    
    # Text hierarchy
    "title": "bold white on #2D5F8D",
    "subtitle": "#DDDDDD on #1A1A1A",
    "help": "dim #AAAAAA",
    "secondary": "#DDDDDD",
    
    # Component styles
    "panel.border": "blue",
    "panel.title": "bold cyan",
})

console = Console(
    theme=custom_theme,
    force_terminal=True,
    width=120,
    legacy_windows=False
)

# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION STATE & SCREENS
# ═══════════════════════════════════════════════════════════════════════════

class Screen(Enum):
    SPLASH = "splash"
    MAIN_DASHBOARD = "main"
    DEVICE_SELECTION = "devices"
    SCAN_MODE = "scan_mode"
    SCAN_PROGRESS = "progress"
    RESULTS = "results"
    FILE_EXPLORER = "explorer"
    PHOTO_GALLERY = "gallery"
    MESSAGES = "messages"
    SETTINGS = "settings"

class ForensicTool:
    def __init__(self):
        self.current_screen = Screen.SPLASH
        self.running = True
        self.selected_device_idx = 0
        self.selected_scan_mode = 0
        self.selected_action = 0
        
        # Mock data
        self.devices = [
            {
                "name": "Samsung Galaxy S21",
                "path": "/dev/sdb",
                "storage": 128,
                "os": "Android 13",
                "id": "••••••••••••",
                "status": "Ready",
                "battery": 87,
                "used_pct": 69.5,
                "last_scan": "2h ago"
            },
            {
                "name": "iPhone 13",
                "path": "/dev/sdc",
                "storage": 256,
                "os": "iOS 17",
                "id": "••••••••••••",
                "status": "Ready",
                "battery": 45,
                "used_pct": 60.9,
                "last_scan": "1d ago"
            },
            {
                "name": "Unknown USB Device",
                "path": "/dev/sdd",
                "storage": 64,
                "os": "Unknown OS",
                "id": "ABC123DEF456",
                "status": "Detected",
                "battery": 0,
                "used_pct": 0,
                "last_scan": "Scanning..."
            }
        ]
        
        self.scan_modes = [
            {
                "name": "🚀  QUICK SCAN",
                "subtitle": "Recommended for most cases",
                "description": "Filesystem enumeration only",
                "time": "~5-15 minutes",
                "impact": "Minimal system load",
                "finds": "All files, folders, basic metadata",
                "suitable": ["Recent files", "metadata", "quick overview"],
                "unsuitable": ["Deleted items", "deep app data"],
            },
            {
                "name": "🔍  DEEP SCAN",
                "subtitle": "Comprehensive forensics",
                "description": "Filesystem + deleted file carving + app extraction",
                "time": "~1-4 hours",
                "impact": "Significant resource usage",
                "finds": "All data including recovered deleted files",
                "suitable": ["Complete recovery", "deleted files", "evidence"],
                "unsuitable": ["Quick turnaround"],
            },
            {
                "name": "⚡  CUSTOM SCAN",
                "subtitle": "Advanced users",
                "description": "Select specific modules and options",
                "time": "Varies",
                "impact": "Configurable",
                "finds": "Based on selected modules",
                "suitable": ["Fine-tuned analysis", "specific targets"],
                "unsuitable": [],
            }
        ]
        
        self.photos = [
            {
                "filename": "IMG_20240115_142340.jpg",
                "size": 2.4,
                "resolution": "4032 x 3024",
                "mp": 12.6,
                "date": "2024-01-15 14:23:40",
                "camera": "Samsung Galaxy S21",
                "gps": "22.5726°N, 88.3639°E",
                "city": "Kolkata, West Bengal, India",
                "status": "Active"
            }
        ]

    # ─────────────────────────────────────────────────────────────────────
    # SCREEN RENDERERS
    # ─────────────────────────────────────────────────────────────────────

    def render_splash_screen(self):
        """Screen 1: Application startup with splash"""
        console.clear()
        
        # ASCII art banner
        console.print("\n\n")
        console.print("                 " + "█" * 35)
        console.print("                 " + "█  FORENSIC RECOVERY TOOL  █")
        console.print("                 " + "█" * 35)
        console.print("                 " + "█  Advanced Mobile Device  █")
        console.print("                 " + "█  Forensic Analysis v2.1  █")
        console.print("                 " + "█" * 35)
        console.print("\n")
        
        # Progress bars
        tasks = [
            ("Loading configuration", 30),
            ("Checking system permissions", 15),
            ("Scanning USB devices", 0),
            ("Loading forensic modules", 0),
            ("Initializing database", 0),
        ]
        
        for task_name, progress in tasks:
            bar = "█" * (progress // 5) + "░" * ((100 - progress) // 5)
            status_icon = "✓" if progress > 0 else ("⟳" if progress == 15 else "○")
            status_color = "green" if progress > 0 else ("blue" if progress == 15 else "white")
            
            line = Text()
            line.append(f"{status_icon}  ", style=status_color)
            line.append(f"{task_name:40} [{bar}] {progress}%")
            console.print(line)
        
        console.print("\n")
        console.print(Align.center(Text("Press ENTER to continue...", style="cyan")))
        input()
        self.current_screen = Screen.MAIN_DASHBOARD

    def render_main_dashboard(self):
        """Screen 2: Main dashboard with device list"""
        console.clear()
        
        title = Panel(
            Text("📱  FORENSIC RECOVERY TOOL - Main Dashboard", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        # Connected Devices Panel
        devices_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        
        for idx, device in enumerate(self.devices):
            status_color = "green" if "Ready" in device["status"] else "yellow"
            
            device_name = f"{'✓' if 'Ready' in device['status'] else '⚠'}  {device['name']} ({device['path']}) - {device['storage']}GB"
            devices_table.add_row(Text(device_name, style=status_color))
            devices_table.add_row(Text(
                f"  └─ {device['os']} | IMEI: {device['id']}",
                style="dim"
            ))
            devices_table.add_row(Text(
                f"  └─ Status: {device['status']} | Last scan: {device['last_scan']}",
                style="dim"
            ))
            devices_table.add_row(Text(
                f"  └─ Space used: {device['used_pct']}% ({int(device['storage'] * device['used_pct']/100)}GB / {device['storage']}GB)",
                style="dim"
            ))
            devices_table.add_row("")
        
        console.print(Panel(
            devices_table,
            title="[bold cyan]Connected Devices[/]",
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()
        
        # Quick Actions
        actions_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        actions = [
            ("▶  Start New Scan", "[Begin forensic analysis]"),
            ("   Analyze Previous Scans", "[View historical data]"),
            ("   Device Information", "[View detailed specs]"),
            ("   Settings & Configuration", "[Customize tool behavior]"),
            ("   Help & Documentation", "[Browse help topics]"),
            ("   Exit Application", "[Quit the tool]"),
        ]
        
        for action, desc in actions:
            actions_table.add_row(Text(action, style="cyan"), Text(desc, style="help"))
        
        console.print(Panel(
            actions_table,
            title="[bold cyan]Quick Actions[/]",
            border_style="blue",
            padding=(1, 2)
        ))
        console.print()
        
        # Navigation
        nav = Text()
        nav.append("[", style="dim")
        nav.append("↑↓", style="cyan")
        nav.append("] Navigate  [", style="dim")
        nav.append("ENTER", style="cyan")
        nav.append("] Select  [", style="dim")
        nav.append("?", style="cyan")
        nav.append("] Help  [", style="dim")
        nav.append("Q", style="red")
        nav.append("] Quit", style="dim")
        console.print(nav)
        
        self._handle_input_dashboard()

    def render_device_selection(self):
        """Screen 3: Device selection with highlight"""
        console.clear()
        
        title = Panel(
            Text("🔌  SELECT DEVICE FOR ANALYSIS", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        for idx, device in enumerate(self.devices):
            if idx == self.selected_device_idx:
                border_style = "bold cyan"
                style = "on #2D5F8D"
                prefix = "▶ "
            else:
                border_style = "blue"
                style = ""
                prefix = "  "
            
            content = Text()
            content.append(f"{device['path']} | ", style="cyan")
            content.append(f"{device['storage']} GB | ", style="yellow")
            content.append(f"{device['os']} | ", style="blue")
            content.append(f"IMEI: {device['id']}\n", style="dim")
            content.append(f"Status: ", style="white")
            status_color = "green" if "Ready" in device['status'] else "yellow"
            content.append(f"{device['status']}\n", style=status_color)
            content.append(f"Battery: {device['battery']}% | ", style="dim")
            content.append(f"Storage Used: {device['used_pct']}%", style="dim")
            
            panel = Panel(
                content,
                title=f"[{border_style}]{prefix}{device['name']}[/]",
                border_style=border_style,
                padding=(1, 2),
                style=style,
                box=box.ROUNDED if idx == self.selected_device_idx else box.SQUARE
            )
            console.print(panel)
            console.print()
        
        nav = Text("[D] Details  [I] Info  [ENTER] Select  [↑↓] Navigate  [ESC] Back")
        nav.stylize("cyan")
        console.print(nav)
        
        self._handle_input_device_selection()

    def render_scan_mode_selection(self):
        """Screen 4: Scan mode selection"""
        console.clear()
        
        device_name = self.devices[self.selected_device_idx]["name"]
        title = Panel(
            Text(f"📊  SELECT ANALYSIS MODE - {device_name}", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        for idx, mode in enumerate(self.scan_modes):
            if idx == self.selected_scan_mode:
                border_style = "bold cyan"
                title_style = "bold cyan"
                bg_style = "on #2D5F8D"
                prefix = "▶ "
            else:
                border_style = "blue"
                title_style = "blue"
                bg_style = ""
                prefix = "  "
            
            # Build content
            content = Text()
            content.append(f"{mode['description']}\n", style="white")
            content.append(f"Time: ", style="dim")
            content.append(f"{mode['time']} | ", style="yellow")
            content.append(f"Impact: ", style="dim")
            content.append(f"{mode['impact']}\n", style="warning")
            content.append(f"Finds: ", style="dim")
            content.append(f"{mode['finds']}\n\n", style="white")
            
            content.append("✓ Suitable: ", style="success")
            content.append(", ".join(mode['suitable']), style="dim")
            content.append("\n✗ Won't: ", style="danger")
            content.append(", ".join(mode['unsuitable']), style="dim")
            
            panel = Panel(
                content,
                title=f"[{title_style}]{prefix}{mode['name']}[/]",
                border_style=border_style,
                padding=(1, 2),
                style=bg_style,
                box=box.ROUNDED if idx == self.selected_scan_mode else box.SQUARE
            )
            console.print(panel)
            console.print()
        
        nav = Text("[↑↓] Navigate  [ENTER] Select  [?] Learn More  [ESC] Back")
        nav.stylize("cyan")
        console.print(nav)
        
        self._handle_input_scan_mode()

    def render_scan_progress(self):
        """Screen 5: Live scan progress"""
        console.clear()
        
        device = self.devices[self.selected_device_idx]
        title = Panel(
            Text(f"⏳  QUICK SCAN IN PROGRESS - {device['name']}", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        # Device info
        info = Text()
        info.append(f"Device: {device['name']} ({device['path']})\n", style="cyan")
        info.append(f"Started: 2024-01-15 14:32:45  |  Elapsed: 3m 24s", style="dim")
        console.print(info)
        console.print()
        
        # Current operation
        op_table = Table(show_header=False, box=box.SIMPLE)
        op_table.add_row(
            Text("Reading filesystem metadata", style="cyan"),
            Text("45%  ~2m 15s remaining", style="yellow")
        )
        op_table.add_row("████████████████████░░░░░░░░░░░░░░░░")
        console.print(Panel(op_table, title="[bold cyan]Current Operation[/]"))
        console.print()
        
        # Step progress
        steps_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        steps = [
            ("✓  1. Device validation & mounted filesystems", "green"),
            ("✓  2. Partition table analysis", "green"),
            ("⟳ 3. Recursive filesystem enumeration", "blue"),
            ("○  4. Metadata extraction", "white"),
            ("○  5. File categorization & indexing", "white"),
            ("○  6. Report generation", "white"),
        ]
        
        for step, color in steps:
            steps_table.add_row(Text(step, style=color))
        
        console.print(Panel(steps_table, title="[bold cyan]Step Progress[/]"))
        console.print()
        
        # Live stats
        stats_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        stats_table.add_row(
            Text("Files Found:", style="dim"),
            Text("47,239", style="green"),
            Text("Folders Scanned:", style="dim"),
            Text("2,847", style="cyan")
        )
        stats_table.add_row(
            Text("Data Processed:", style="dim"),
            Text("89.3 GB", style="blue"),
            Text("Processing Speed:", style="dim"),
            Text("24.5 MB/s", style="yellow")
        )
        console.print(Panel(stats_table, title="[bold cyan]Live Statistics[/]"))
        console.print()
        
        nav = Text("[P] Pause  [C] Cancel  [S] Save & Continue", style="cyan")
        console.print(nav)
        
        # Simulate progress
        time.sleep(2)
        self.current_screen = Screen.RESULTS

    def render_results_dashboard(self):
        """Screen 6: Scan results"""
        console.clear()
        
        title = Panel(
            Text("✓  SCAN COMPLETE - Samsung Galaxy S21", 
                 style="success", justify="center"),
            border_style="green",
            style="on #1A5F2D"
        )
        console.print(title)
        console.print()
        
        # Scan details
        details = Text("Scan Details: 3h 47m 23s | Completed: 2024-01-15 18:20:08 | Status: ", 
                      style="white")
        details.append("✓ Success", style="bold green")
        console.print(details)
        console.print()
        
        # Summary table
        summary_table = Table(
            title="Summary Statistics",
            title_style="bold cyan",
            box=box.SIMPLE,
            padding=(0, 1)
        )
        summary_table.add_column("Category", style="cyan")
        summary_table.add_column("Count", style="yellow", justify="right")
        summary_table.add_column("Progress", style="green")
        summary_table.add_column("Size", style="blue", justify="right")
        
        data = [
            ("Photos & Videos", "1,847 files", "████████░░", "24.3 GB"),
            ("Documents", "342 files", "██░░░░░░░░", "1.2 GB"),
            ("Messages", "8,924 records", "░░░░░░░░░░", "0.8 GB"),
            ("Contacts", "347 entries", "░░░░░░░░░░", "0.2 MB"),
            ("Browser History", "2,341 entries", "░░░░░░░░░░", "0.4 GB"),
            ("Deleted Files", "3,284 items", "███░░░░░░░", "4.7 GB"),
        ]
        
        for cat, count, prog, size in data:
            summary_table.add_row(cat, count, prog, size)
        
        console.print(Panel(summary_table))
        console.print()
        
        # Key findings
        findings = Text()
        findings.append("⚠  ", style="warning")
        findings.append("156 deleted photos recovered (last modified: 1 month ago)\n", style="white")
        findings.append("ℹ  ", style="info")
        findings.append("8 encrypted app containers detected (3 decryptable)\n", style="white")
        findings.append("✓  ", style="success")
        findings.append("GPS coordinates extracted from 1,247 photos\n", style="white")
        
        console.print(Panel(findings, title="[bold yellow]Key Findings[/]", border_style="#FF851B"))
        console.print()
        
        # Actions
        actions_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        actions_table.add_row("[bold cyan]💾  Save Report to File[/]")
        actions_table.add_row("[bold cyan]🔍  View Media Gallery[/]")
        actions_table.add_row("[bold cyan]📂  Open in File Manager[/]")
        
        console.print(Panel(actions_table, title="[bold cyan]Quick Actions[/]"))
        console.print()
        
        nav = Text("[↑↓] Navigate  [ENTER] Select  [ESC] Back", style="cyan")
        console.print(nav)
        
        self._handle_input_results()

    def render_file_explorer(self):
        """Screen 7: File tree explorer"""
        console.clear()
        
        title = Panel(
            Text("📂  FILE EXPLORER - Samsung Galaxy S21", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        # Create tree
        tree = Tree("📁 / (root) - 128 GB, 47,239 files", guide_style="blue")
        
        system = tree.add("📁 system/ - 1.2 GB, 234 files", style="cyan")
        system.add("▶ 📁 fonts/ - 234 MB, 47 files")
        system.add("▶ 📁 app/ - 678 MB, 156 files")
        
        data = tree.add("📁 data/ - 45.3 GB, 23,847 files", style="cyan")
        app = data.add("📁 app/ - 22.4 GB, 847 files", style="cyan")
        
        whatsapp = app.add("[bold yellow]📁 com.whatsapp/ - 1.2 GB[/]")
        whatsapp.add("[bold green]✓ msgstore.db - 234 MB[/]")
        whatsapp.add("[bold red]🔒 msgstore.db.crypt12 - 456 MB[/]")
        whatsapp.add("▶ 📁 media/ - 980 MB, 1,247 items")
        
        instagram = app.add("📁 com.instagram/ - 2.3 GB", style="cyan")
        instagram.add("📄 cache.json - 12.3 MB")
        instagram.add("[bold cyan]🖼  profile_pic.jpg - 1.2 MB[/]")
        instagram.add("▶ 📁 posts/ - 1.8 GB, 342 photos")
        
        media = data.add("📁 media/ - 14.2 GB, 8,923 files", style="cyan")
        pictures = media.add("[bold yellow]📁 Pictures/ - 8.9 GB, 1,847 photos[/]")
        pictures.add("[bold cyan]🖼  IMG_20240115_142340.jpg - 2.4 MB ✦[/]")
        pictures.add("🖼  IMG_20240115_143015.jpg - 3.1 MB")
        pictures.add("[dim]🖼  IMG_20240114_221502.jpg - 1.8 MB [DELETED][/]")
        
        console.print(Panel(tree, title="[bold cyan]Directory Tree[/]", border_style="blue"))
        console.print()
        
        nav = Text("[↑↓→←] Navigate  [ENTER] Details  [*] Mark  [D] Download  [ESC] Back")
        nav.stylize("cyan")
        console.print(nav)
        
        self._handle_input_explorer()

    def render_photo_gallery(self):
        """Screen 8: Photo gallery"""
        console.clear()
        
        photo = self.photos[0]
        
        title = Panel(
            Text(f"🖼️   {photo['filename']}", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        # Photo preview box
        preview = Panel(
            Text("[Photo Preview]\n4032 x 3024 (12.6 MP)", 
                 style="dim", justify="center"),
            border_style="cyan",
            padding=(5, 15)
        )
        console.print(preview)
        console.print()
        
        # Metadata
        meta_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        meta_table.add_column("Field", style="cyan", width=18)
        meta_table.add_column("Value", style="white")
        
        metadata = [
            ("Filename", photo['filename']),
            ("Size", f"{photo['size']} MB"),
            ("Format", "JPEG"),
            ("Resolution", f"{photo['resolution']} pixels ({photo['mp']} MP)"),
            ("Date Taken", photo['date']),
            ("Camera", photo['camera']),
            ("GPS Location", Text(f"📍 {photo['gps']}", style="green")),
            ("City", Text(photo['city'], style="dim")),
            ("Status", Text(photo['status'], style="green")),
        ]
        
        for field, value in metadata:
            meta_table.add_row(field, str(value))
        
        console.print(Panel(meta_table, title="[bold cyan]Metadata[/]", border_style="blue"))
        console.print()
        
        # Navigation
        nav = Text()
        nav.append("[", style="dim")
        nav.append("📍 View Map", style="cyan")
        nav.append("]  [", style="dim")
        nav.append("💾 Save", style="cyan")
        nav.append("]  [", style="dim")
        nav.append("⬅ Prev", style="cyan")
        nav.append("]  [", style="dim")
        nav.append("Next ➡", style="cyan")
        nav.append("]  [", style="dim")
        nav.append("ESC", style="red")
        nav.append("] Back", style="dim")
        console.print(nav)
        console.print()
        
        progress = Text("Image 1 / 1,847  ", style="dim")
        progress.append("████████████░░░░░░░░░░░░░░░░░░░░░░░░", style="cyan")
        progress.append(" 0.05%", style="yellow")
        console.print(progress)
        
        self._handle_input_gallery()

    def render_messages(self):
        """Screen 9: Message viewer"""
        console.clear()
        
        title = Panel(
            Text("💬  MESSAGE EXTRACTION - WhatsApp", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        # Header
        header = Text()
        header.append("Conversations Found: ", style="dim")
        header.append("47", style="cyan")
        header.append("  │  Total Messages: ", style="dim")
        header.append("8,924", style="cyan")
        header.append("  │  Last Updated: ", style="dim")
        header.append("2024-01-15 18:20", style="yellow")
        console.print(header)
        console.print()
        
        # Conversations
        convos_table = Table(box=box.SIMPLE, padding=(0, 1))
        convos_table.add_column("Contact", style="cyan")
        convos_table.add_column("Last Message", style="white")
        convos_table.add_column("Count", style="yellow", justify="right")
        
        conversations = [
            ("👤  Mom", "Today 3:45 PM", "247 msgs"),
            ("👥  Team Group Chat", "Today 10:22 AM", "3,847 msgs"),
            ("👤  John Doe", "2 days ago", "1,247 msgs"),
        ]
        
        for contact, last, count in conversations:
            convos_table.add_row(contact, last, count)
        
        console.print(Panel(convos_table, title="[bold cyan]Conversations[/]"))
        console.print()
        
        # Messages
        msg_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        msg_table.add_column("Time", style="dim", width=12)
        msg_table.add_column("Sender", style="cyan", width=15)
        msg_table.add_column("Message", style="white")
        
        messages = [
            ("12:15 PM", "You", "Sure, I'll send it by EOD"),
            ("12:16 PM", "Mom", "Thanks! Don't forget the documents"),
            ("12:47 PM", "You", "Sending now..."),
            ("1:02 PM", "Mom", Text("Perfect! See you tonight", style="green")),
        ]
        
        for time, sender, msg in messages:
            msg_table.add_row(time, sender, msg)
        
        console.print(Panel(msg_table, title="[bold cyan]Mom - 247 messages[/]"))
        console.print()
        
        nav = Text("[↑↓] Scroll  [E] Export  [D] Download  [ESC] Back", style="cyan")
        console.print(nav)
        
        self._handle_input_messages()

    def render_settings(self):
        """Screen 10: Settings"""
        console.clear()
        
        title = Panel(
            Text("⚙️   SETTINGS & CONFIGURATION", 
                 style="title", justify="center"),
            border_style="blue"
        )
        console.print(title)
        console.print()
        
        # General settings
        general_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        general_table.add_column("Setting", style="cyan", width=28)
        general_table.add_column("Value", style="white")
        
        general_table.add_row("Output Directory", "/home/user/forensic_reports/")
        general_table.add_row("Temporary Directory", "/tmp/forensic_temp/")
        
        console.print(Panel(general_table, title="[bold cyan]General Settings[/]", border_style="blue"))
        console.print()
        
        # Scan settings
        scan_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        scan_table.add_column("Setting", style="cyan", width=28)
        scan_table.add_column("Value", style="white")
        
        scan_table.add_row("Default Scan Mode", Text("Quick Scan", style="yellow"))
        scan_table.add_row("Auto-delete temp", Text("☑ Enabled", style="green"))
        scan_table.add_row("Enable file carving", Text("☑ Enabled", style="green"))
        scan_table.add_row("Default threads", "[4] Auto-detect")
        
        console.print(Panel(scan_table, title="[bold cyan]Scan Settings[/]", border_style="blue"))
        console.print()
        
        # Security settings
        security_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        security_table.add_column("Setting", style="cyan", width=28)
        security_table.add_column("Value", style="white")
        
        security_table.add_row("Encrypt temp files", Text("☑ Enabled", style="green"))
        security_table.add_row("Enable audit logging", Text("☑ Enabled", style="green"))
        security_table.add_row("Secure deletion", Text("DoD 5220.22-M", style="orange"))
        
        console.print(Panel(security_table, title="[bold cyan]Security & Privacy[/]", border_style="blue"))
        console.print()
        
        # Advanced
        advanced_table = Table(show_header=False, box=box.SIMPLE)
        advanced_table.add_row("[cyan]📋 View Logs[/]", "[cyan]🔄 Reset[/]", "[cyan]🗑  Clear[/]")
        advanced_table.add_row("[cyan]✓ Verify[/]", "[cyan]🔍 Updates[/]", "[cyan]💾 Save[/]")
        
        console.print(Panel(advanced_table, title="[bold cyan]Advanced Options[/]"))
        console.print()
        
        nav = Text("[SPACE] Toggle  [↑↓] Navigate  [ENTER] Edit  [S] Save  [ESC] Back")
        nav.stylize("cyan")
        console.print(nav)
        
        self._handle_input_settings()

    # ─────────────────────────────────────────────────────────────────────
    # INPUT HANDLERS
    # ─────────────────────────────────────────────────────────────────────

    def _handle_input_dashboard(self):
        """Handle main dashboard input"""
        try:
            user_input = input().lower()
            if user_input == 'q':
                self.running = False
            elif user_input == '':
                self.current_screen = Screen.DEVICE_SELECTION
            elif user_input == '?':
                console.print("[cyan]Help: Use arrow keys to navigate, ENTER to select[/]")
        except (EOFError, KeyboardInterrupt):
            self.running = False

    def _handle_input_device_selection(self):
        """Handle device selection input"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.MAIN_DASHBOARD
            elif user_input == '' or user_input == 'enter':
                self.current_screen = Screen.SCAN_MODE
            elif user_input == 'w' or user_input == 'arrowup':
                self.selected_device_idx = (self.selected_device_idx - 1) % len(self.devices)
            elif user_input == 's' or user_input == 'arrowdown':
                self.selected_device_idx = (self.selected_device_idx + 1) % len(self.devices)
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.MAIN_DASHBOARD

    def _handle_input_scan_mode(self):
        """Handle scan mode selection"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.DEVICE_SELECTION
            elif user_input == '' or user_input == 'enter':
                self.current_screen = Screen.SCAN_PROGRESS
            elif user_input == 'w' or user_input == 'arrowup':
                self.selected_scan_mode = (self.selected_scan_mode - 1) % len(self.scan_modes)
            elif user_input == 's' or user_input == 'arrowdown':
                self.selected_scan_mode = (self.selected_scan_mode + 1) % len(self.scan_modes)
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.DEVICE_SELECTION

    def _handle_input_results(self):
        """Handle results screen input"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.MAIN_DASHBOARD
            elif user_input == '1' or user_input == '':
                self.current_screen = Screen.FILE_EXPLORER
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.MAIN_DASHBOARD

    def _handle_input_explorer(self):
        """Handle file explorer input"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.RESULTS
            elif user_input == 'g':
                self.current_screen = Screen.PHOTO_GALLERY
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.RESULTS

    def _handle_input_gallery(self):
        """Handle gallery input"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.FILE_EXPLORER
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.FILE_EXPLORER

    def _handle_input_messages(self):
        """Handle messages input"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.MAIN_DASHBOARD
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.MAIN_DASHBOARD

    def _handle_input_settings(self):
        """Handle settings input"""
        try:
            user_input = input().lower()
            if user_input == 'escape' or user_input == '\x1b':
                self.current_screen = Screen.MAIN_DASHBOARD
        except (EOFError, KeyboardInterrupt):
            self.current_screen = Screen.MAIN_DASHBOARD

    # ─────────────────────────────────────────────────────────────────────
    # MAIN LOOP
    # ─────────────────────────────────────────────────────────────────────

    def run(self):
        """Main application loop"""
        while self.running:
            if self.current_screen == Screen.SPLASH:
                self.render_splash_screen()
            elif self.current_screen == Screen.MAIN_DASHBOARD:
                self.render_main_dashboard()
            elif self.current_screen == Screen.DEVICE_SELECTION:
                self.render_device_selection()
            elif self.current_screen == Screen.SCAN_MODE:
                self.render_scan_mode_selection()
            elif self.current_screen == Screen.SCAN_PROGRESS:
                self.render_scan_progress()
            elif self.current_screen == Screen.RESULTS:
                self.render_results_dashboard()
            elif self.current_screen == Screen.FILE_EXPLORER:
                self.render_file_explorer()
            elif self.current_screen == Screen.PHOTO_GALLERY:
                self.render_photo_gallery()
            elif self.current_screen == Screen.MESSAGES:
                self.render_messages()
            elif self.current_screen == Screen.SETTINGS:
                self.render_settings()
        
        console.clear()
        console.print("\n[green]Thank you for using the Forensic Recovery Tool![/]\n")


def main():
    """Application entry point"""
    app = ForensicTool()
    app.run()


if __name__ == "__main__":
    main()