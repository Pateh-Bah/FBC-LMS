#!/usr/bin/env python
"""
Script to create sample ebooks with placeholder PDFs for the FBC Library System
"""

import os
import sys
import django
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
except Exception as e:
    print("reportlab is required. Install it with: pip install reportlab")
    raise

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_system.settings")
django.setup()

from fbc_books.models import Book, Category, Author
from django.core.files.base import ContentFile
from django.utils.text import slugify


def create_sample_pdf(title, author, content_preview):
    """Create a sample PDF with basic content"""
    buffer = BytesIO()

    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_para = Paragraph(f"<b><font size=20>{title}</font></b>", styles["Title"])
    story.append(title_para)
    story.append(Spacer(1, 20))

    # Author
    author_para = Paragraph(f"<i>by {author}</i>", styles["Normal"])
    story.append(author_para)
    story.append(Spacer(1, 40))

    # Content preview
    content_para = Paragraph(content_preview, styles["Normal"])
    story.append(content_para)
    story.append(Spacer(1, 20))

    # Note about sample
    note_para = Paragraph(
        "<i>This is a sample ebook for demonstration purposes in the FBC Library System. "
        "In a real implementation, this would contain the full book content.</i>",
        styles["Italic"],
    )
    story.append(note_para)

    doc.build(story)
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content


def create_ebook(title, isbn, author_name, category_name, description, content_preview):
    """Create an ebook entry in the database"""
    try:
        # Get or create category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={"description": f"Books in the {category_name} category"},
        )
        if created:
            print(f"Created category: {category_name}")

        # Get or create author
        author, created = Author.objects.get_or_create(
            name=author_name, defaults={"bio": f"Author of {title}"}
        )
        if created:
            print(f"Created author: {author_name}")

        # Check if book already exists
        if Book.objects.filter(isbn=isbn).exists():
            print(f"Book with ISBN {isbn} already exists. Skipping...")
            return None

        # Create PDF content
        print(f"Creating PDF for {title}...")
        pdf_content = create_sample_pdf(title, author_name, content_preview)

        # Create book
        book = Book.objects.create(
            title=title,
            isbn=isbn,
            category=category,
            description=description,
            book_type="ebook",
            total_copies=1,
            available_copies=1,
            status="available",
        )

    # Add author
    book.authors.add(author)

    # Save PDF file
    filename = f"{slugify(title)}.pdf"
    book.pdf_file.save(filename, ContentFile(pdf_content), save=True)

    print(f"Successfully created ebook: {title}")
    return book

    except Exception as e:
        print(f"Error creating ebook {title}: {e}")
        return None


def main():
    """Main function to add sample ebooks"""
    print("Creating sample ebooks for FBC Library System...")
    print("=" * 50)

    # Sample ebooks with content previews
    ebooks = [
        {
            "title": "Pride and Prejudice",
            "isbn": "9781234567890",
            "author": "Jane Austen",
            "category": "Classic Literature",
            "description": "A romantic novel of manners written by Jane Austen in 1813. It follows the character development of Elizabeth Bennet, the dynamic protagonist, who learns about the repercussions of hasty judgments.",
            "content_preview": """It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.

"My dear Mr. Bennet," said his lady to him one day, "have you heard that Netherfield Park is let at last?"

Mr. Bennet replied that he had not.

"But it is," returned she; "for Mrs. Long has just been here, and she told me all about it."

Mr. Bennet made no answer.

"Do you not want to know who has taken it?" cried his wife impatiently.

"You want to tell me, and I have no objection to hearing it."

This was invitation enough for Elizabeth to share her thoughts...""",
        },
        {
            "title": "The Adventures of Sherlock Holmes",
            "isbn": "9781234567891",
            "author": "Arthur Conan Doyle",
            "category": "Mystery",
            "description": "A collection of twelve short stories featuring the famous detective Sherlock Holmes, written by Arthur Conan Doyle and published in 1892.",
            "content_preview": """To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler. All emotions, and that one particularly, were abhorrent to his cold, precise but admirably balanced mind.

He was, I take it, the most perfect reasoning and observing machine that the world has seen, but as a lover he would have placed himself in a false position. He never spoke of the softer passions, save with a gibe and a sneer.

They were admirable things for the observer—excellent for drawing the veil from men's motives and actions. But for the trained reasoner to admit such intrusions into his own delicate and finely adjusted temperament was to introduce a distracting factor which might throw a doubt upon all his mental results.""",
        },
        {
            "title": "Alice's Adventures in Wonderland",
            "isbn": "9781234567892",
            "author": "Lewis Carroll",
            "category": "Children's Literature",
            "description": "A novel written by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll. It tells of a young girl named Alice who falls down a rabbit hole.",
            "content_preview": """Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversation?'

So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.

There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!' (when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it.""",
        },
        {
            "title": "The Time Machine",
            "isbn": "9781234567893",
            "author": "H.G. Wells",
            "category": "Science Fiction",
            "description": "A science fiction novella by H. G. Wells, published in 1895. The work is generally credited with the popularization of the concept of time travel.",
            "content_preview": '''The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. His grey eyes shone and twinkled, and his usually pale face was flushed and animated. The fire burned brightly, and the soft radiance of the incandescent lights in the lilies of silver caught the bubbles that flashed and passed in our glasses.

Our chairs, being his patents, embraced and caressed us rather than submitted to be sat upon, and there was that luxurious after-dinner atmosphere when thought runs gracefully free of the trammels of precision. And he put it to us in this way—marking the points with a lean forefinger—as we sat and lazily admired his earnestness over this new paradox (as we thought it) and his fecundity.

"You must follow me carefully. I shall have to controvert one or two ideas that are almost universally accepted. The geometry, for instance, they taught you at school is founded on a misconception."''',
        },
    ]

    success_count = 0
    for ebook_data in ebooks:
        print(f"\nProcessing: {ebook_data['title']}")
        book = create_ebook(
            title=ebook_data["title"],
            isbn=ebook_data["isbn"],
            author_name=ebook_data["author"],
            category_name=ebook_data["category"],
            description=ebook_data["description"],
            content_preview=ebook_data["content_preview"],
        )
        if book:
            success_count += 1

    print("\n" + "=" * 50)
    print(f"Successfully added {success_count} out of {len(ebooks)} ebooks!")

    # Display current ebook count
    total_ebooks = Book.objects.filter(book_type="ebook").count()
    print(f"Total ebooks in system: {total_ebooks}")
    print("Done!")


if __name__ == "__main__":
    main()
